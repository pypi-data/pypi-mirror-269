import json
import logging
import os
import sys
import time
from abc import ABC
from dataclasses import dataclass
from enum import Enum, unique
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import cv2
import numpy as np
import socketio
import ujson
from lz4.frame import compress, decompress

from era_5g_interface.exceptions import BackPressureException, UnknownChannelTypeUsed
from era_5g_interface.frame_decoder import FrameDecoder, FrameDecoderError
from era_5g_interface.frame_encoder import FrameEncoder, FrameEncoderError
from era_5g_interface.measuring import Measuring

logger = logging.getLogger(__name__)

# TODO: use enums?
DATA_NAMESPACE = str("/data")
DATA_ERROR_EVENT = str("data_error")

CONTROL_NAMESPACE = str("/control")
COMMAND_EVENT = str("command")
COMMAND_ERROR_EVENT = str("command_error")
COMMAND_RESULT_EVENT = str("command_result")


@unique
class ChannelType(Enum):
    """Channel type dataclass."""

    JSON = 1
    JPEG = 2
    H264 = 3
    JSON_LZ4 = 4
    HEVC = 5


@dataclass
class CallbackInfoClient:
    """Callback info dataclass used on client side."""

    type: ChannelType
    callback: Callable[[Dict], Any]  # Custom callback with dict.
    error_event: str = DATA_ERROR_EVENT  # Custom error event name.


@dataclass
class CallbackInfoServer:
    """Callback info dataclass used on server side - callback has namespace sid parameter."""

    type: ChannelType
    callback: Callable[[str, Dict], Any]  # Custom callback with sid and dict.
    error_event: str = DATA_ERROR_EVENT  # Custom error event name.


class Channels(ABC):
    """Channels class is used to define channel data callbacks and contains send functions.

    It handles image frames JPEG, H.264 and HEVC encoding/decoding. Data is sent via the DATA_NAMESPACE. The class
    cannot be used alone. The ServerChannels and ClientChannels classes create callbacks and encoders/decoders.
    """

    # This should work roughly like an abstract member.
    _callbacks_info: Union[Dict[str, CallbackInfoClient], Dict[str, CallbackInfoServer]]

    def __init__(
        self,
        sio: Union[socketio.Client, socketio.Server],
        callbacks_info: Union[Dict[str, CallbackInfoClient], Dict[str, CallbackInfoServer]],
        disconnect_callback: Optional[Callable] = None,
        back_pressure_size: Optional[int] = 5,
        recreate_coder_attempts_count: int = 5,
        stats: bool = False,
        extended_measuring: bool = False,
    ):
        """Constructor.

        Args:
            sio (Union[socketio.Client, socketio.Server]): Socketio Client or Server object.
            callbacks_info (Union[Dict[str, CallbackInfoClient], Dict[str, CallbackInfoServer]]): Callbacks Info
                dictionary, key is custom event name.
            disconnect_callback (Callable, optional): Triggered before _shutdown on unhandled exception.
            back_pressure_size (int, optional): Back pressure size - max size of eio.queue.qsize().
            recreate_coder_attempts_count (int): How many times try to recreate the frame encoder/decoder.
            stats (bool): Store output data sizes.
            extended_measuring (bool): Enable logging of measuring.
        """

        self._sio = sio
        self._disconnect_callback = disconnect_callback

        if back_pressure_size is not None and back_pressure_size < 1:
            raise ValueError("Invalid value for back_pressure_size.")

        self._back_pressure_size = back_pressure_size
        self._recreate_coder_attempts_count = recreate_coder_attempts_count
        self._stats = stats
        if self._stats:
            self._sizes: List[int] = []
        self._extended_measuring = extended_measuring

        if isinstance(self._sio, socketio.Client):
            measuring_filename_prefix = "client-"
        else:
            measuring_filename_prefix = "server-"

        self._input_measuring = Measuring(
            measuring_items={
                "key_timestamp": 0,
                "eio_sid": 0,
                "event": "",
                "before_decode_timestamp": 0,
                "after_decode_timestamp": 0,
                "before_lz4_decode_timestamp": 0,
                "after_lz4_decode_timestamp": 0,
                "before_callback_timestamp": 0,
                "after_callback_timestamp": 0,
            },
            enabled=self._extended_measuring,
            filename_prefix=measuring_filename_prefix + "channels-input",
        )

        self._output_measuring = Measuring(
            measuring_items={
                "key_timestamp": 0,
                "eio_sid": 0,
                "event": "",
                "worker_recv_timestamp": 0,
                "worker_before_process_timestamp": 0,
                "worker_after_process_timestamp": 0,
                "worker_send_timestamp": 0,
                "before_encode_timestamp": 0,
                "after_encode_timestamp": 0,
                "size": 0,
                "before_lz4_encode_timestamp": 0,
                "after_lz4_encode_timestamp": 0,
                "before_send_timestamp": 0,
                "after_send_timestamp": 0,
            },
            enabled=self._extended_measuring,
            filename_prefix=measuring_filename_prefix + "channels-output",
        )

        self._callbacks_info = callbacks_info
        # For multiple frame streams, the encoders and the decoders are indexed by Tuple(eio_sid, event).
        self._decoders: Dict[Tuple[str, str], FrameDecoder] = dict()
        self._encoders: Dict[Tuple[str, str], FrameEncoder] = dict()

    def _shutdown(self, cb_type: str, event: str, sid: Optional[str] = None) -> None:
        logger.error(f"Unhandled exception in {cb_type} callback (event: {event}).", exc_info=sys.exc_info())
        if self._disconnect_callback:
            if isinstance(self._sio, socketio.Client):
                self._disconnect_callback()
            else:
                self._disconnect_callback(sid, DATA_NAMESPACE)
        logging.shutdown()  # should flush the logger
        os._exit(1)  # standard sys.exit() is not enough

    def _apply_back_pressure(self, sid: Optional[str] = None) -> None:
        """Apply back pressure."""

        if self._back_pressure_size is not None:
            if isinstance(self._sio, socketio.Client):
                if self._sio.eio.queue.qsize() > self._back_pressure_size:
                    raise BackPressureException()
            else:
                if sid is None:
                    raise ValueError("'sid' has to be set for server.")
                eio_sid = self.get_client_eio_sid(str(sid), DATA_NAMESPACE)
                if self._sio.eio.sockets[eio_sid].queue.qsize() > self._back_pressure_size:
                    raise BackPressureException()

    @staticmethod
    def get_timestamp_from_data(data: Dict, name: str = "timestamp", default: Optional[int] = None):
        if default is None:
            default = time.perf_counter_ns()
        timestamp = data.get(name, 0)
        if not timestamp:
            try:
                timestamp = json.loads(data.get("data", "")).get(name, default)
            except (ValueError, TypeError):
                timestamp = default
        return timestamp

    def send_image(
        self,
        frame: np.ndarray,
        event: str,
        channel_type: ChannelType,
        timestamp: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
        sid: Optional[str] = None,
        can_be_dropped: bool = True,
        wait_for_reconnection: bool = True,
        blocking: bool = False,
        encoding_options: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Send general image data with JPEG or H.264 or HEVC encoding via DATA_NAMESPACE.

        NOTE: DATA_NAMESPACE is assumed to be a connected namespace.

        Args:
            frame (np.ndarray): Video frame / image.
            event (str): Event name.
            channel_type (ChannelType): Encoding type - ChannelType.JPEG or ChannelType.H264 or ChannelType.HEVC.
            timestamp (int): Frame timestamp.
            metadata (Dict[str, Any], optional): Optional metadata to send.
            sid (str, optional): Namespace sid - mandatory when sending from the server side to the client.
            can_be_dropped (bool): If data can be lost due to back pressure.
            wait_for_reconnection (bool): Wait for reconnection to server side? Wait is blocking.
            blocking (bool): If True, wait for the response. Defaults to False.
            encoding_options (Dict[str, str], optional): Video codec options, e.g. {"crf": "0", "preset":
                "ultrafast", "tune": "zerolatency", "x264-params": "keyint=5"}, default: {"preset": "ultrafast",
                "tune": "zerolatency"}.

        Parameter frame.shape should not be changed after first send_image function call.
        Parameters encoding_options and frame.shape are only used in the first send_image call to create the encoder.
        """

        if channel_type not in (ChannelType.JPEG, ChannelType.H264, ChannelType.HEVC):
            raise UnknownChannelTypeUsed()

        if timestamp is None:
            timestamp = time.perf_counter_ns()
        data: Dict[str, Any] = {"timestamp": timestamp}
        if metadata:
            data["metadata"] = metadata
        eio_sid = self.get_client_eio_sid(sid, DATA_NAMESPACE)
        encoder_id = (eio_sid, event)
        if channel_type in (ChannelType.H264, ChannelType.HEVC):
            if encoder_id not in self._encoders:
                try:
                    if channel_type is ChannelType.H264:
                        logger.info(f"Creating H.264 encoder for image size {frame.shape[1]}x{frame.shape[0]}")
                        self._encoders[encoder_id] = FrameEncoder(
                            frame.shape[1], frame.shape[0], codec="h264", options=encoding_options
                        )
                    elif channel_type is ChannelType.HEVC:
                        logger.info(f"Creating HEVC encoder for image size {frame.shape[1]}x{frame.shape[0]}")
                        self._encoders[encoder_id] = FrameEncoder(
                            frame.shape[1], frame.shape[0], codec="hevc", options=encoding_options
                        )
                except Exception as e:
                    logger.error(f"Cannot create video frame encoder: {repr(e)}")
                    raise e
        try:
            is_key_frame = False

            self._output_measuring.log_timestamp(timestamp, "before_encode_timestamp")

            if channel_type in (ChannelType.H264, ChannelType.HEVC):
                frame_encoded = self._encoders[encoder_id].encode_ndarray(frame)
                # TODO: dataclass for this data
                data["width"] = self._encoders[encoder_id].width()
                data["height"] = self._encoders[encoder_id].height()
                is_key_frame = self._encoders[encoder_id].last_frame_is_keyframe()
            else:
                _, frame_jpeg = cv2.imencode(".jpg", frame)
                frame_encoded = frame_jpeg.tobytes()

            self._output_measuring.log_timestamp(timestamp, "after_encode_timestamp")

            data["frame"] = frame_encoded

            if self._stats:
                # TODO: include all data size
                self._sizes.append(len(frame_encoded))
                logger.debug(f"Frame data size: {self._sizes[-1]}")

                self._output_measuring.log_measuring(timestamp, "size", self._sizes[-1])

            if len(frame_encoded):
                self.send_data(
                    data,
                    event,
                    sid=sid,
                    can_be_dropped=(can_be_dropped and not is_key_frame),
                    wait_for_reconnection=wait_for_reconnection,
                    blocking=blocking,
                )
            else:
                logger.warning(
                    "Encoded frame size is zero. It is possible that the encoder settings allow a delay "
                    "of several frames at the beginning of the stream. This means that the timestamps "
                    "will be shifted and will not match the original frames."
                )
        except FrameEncoderError as e:
            logger.error(f"Video frame encoder error: {e}")
            # Try to recreate encoder
            if self._encoders[encoder_id].get_init_count() < self._recreate_coder_attempts_count:
                logger.info(f"Try to recreate encoder ... attempt {self._encoders[encoder_id].get_init_count()}")
                self._encoders[encoder_id].encoder_init()
            else:
                raise e

    def send_data(
        self,
        data: Dict[str, Any],
        event: str,
        channel_type: ChannelType = ChannelType.JSON,
        sid: Optional[str] = None,
        can_be_dropped: bool = False,
        wait_for_reconnection: bool = True,
        blocking: bool = False,
    ) -> Any:
        """Send general JSON data via DATA_NAMESPACE.

        NOTE: DATA_NAMESPACE is assumed to be a connected namespace.

        Args:
            data (Dict[str, Any]): JSON data.
            event (str): Event name.
            channel_type (ChannelType): ChannelType.JSON for raw JSON or ChannelType.JSON_LZ4 for LZ4 compressed JSON.
            sid (str, optional): Namespace sid - mandatory when sending from the server side to the client.
            can_be_dropped (bool): If data can be lost due to back pressure.
            wait_for_reconnection (bool): Wait for reconnection to server side? Wait is blocking.
            blocking (bool): If True, wait for the response. Defaults to False.
        """

        if channel_type is not ChannelType.JSON and channel_type is not ChannelType.JSON_LZ4:
            raise UnknownChannelTypeUsed()

        timestamp = Channels.get_timestamp_from_data(data)

        self._output_measuring.log_measuring(
            timestamp, "worker_recv_timestamp", Channels.get_timestamp_from_data(data, "recv_timestamp", 0)
        )
        self._output_measuring.log_measuring(
            timestamp,
            "worker_before_process_timestamp",
            Channels.get_timestamp_from_data(data, "timestamp_before_process", 0),
        )
        self._output_measuring.log_measuring(
            timestamp,
            "worker_after_process_timestamp",
            Channels.get_timestamp_from_data(data, "timestamp_after_process", 0),
        )
        self._output_measuring.log_measuring(
            timestamp, "worker_send_timestamp", Channels.get_timestamp_from_data(data, "send_timestamp", 0)
        )

        if can_be_dropped:
            self._apply_back_pressure(sid)

        new_data = data
        if channel_type is ChannelType.JSON_LZ4:
            self._output_measuring.log_timestamp(timestamp, "before_lz4_encode_timestamp")
            new_data = compress(bytes(ujson.dumps(data), "utf-8"))
            self._output_measuring.log_timestamp(timestamp, "after_lz4_encode_timestamp")

        self._output_measuring.log_timestamp(timestamp, "before_send_timestamp")

        if isinstance(self._sio, socketio.Client):
            if wait_for_reconnection:
                while not self._sio.connected or not self._sio.eio.state:
                    logger.info("Waiting for reconnection ...")
                    if not self._sio._reconnect_task or not self._sio._reconnect_task.is_alive():
                        break
                    time.sleep(1)
            if blocking:
                return self._sio.call(event, new_data, namespace=DATA_NAMESPACE)
            else:
                self._sio.emit(event, new_data, namespace=DATA_NAMESPACE)
        else:
            if sid is None:
                raise ValueError("'sid' has to be set for server.")
            if not self._sio.manager.is_connected(sid, DATA_NAMESPACE):
                raise ConnectionError(f"Client with {DATA_NAMESPACE} sid {sid} is not connected to server.")
            if blocking:
                self._sio.call(event, new_data, namespace=DATA_NAMESPACE, to=sid)
            else:
                self._sio.emit(event, new_data, namespace=DATA_NAMESPACE, to=sid)

        self._output_measuring.log_timestamp(timestamp, "after_send_timestamp")
        self._output_measuring.log_measuring(timestamp, "eio_sid", self.get_client_eio_sid(sid, DATA_NAMESPACE))
        self._output_measuring.log_measuring(timestamp, "event", event)
        self._output_measuring.store_measuring(timestamp)

    def get_client_eio_sid(self, sid: Optional[str] = None, namespace: Optional[str] = None) -> str:
        """Get client eio sid.

        Args:
            sid (str, optional): Namespace sid - mandatory for using on the server side.
            namespace (str, optional): Namespace - mandatory for using on the server side.

        Returns:
            Client eio sid.
        """

        if isinstance(self._sio, socketio.Client):
            return str(self._sio.sid)
        else:
            if sid is None:
                raise ValueError("'sid' has to be set for server.")
            return str(self._sio.manager.eio_sid_from_sid(sid, namespace))

    def data_error_callback(self, data: Dict[str, Any], sid: Optional[str] = None) -> None:
        """Allows to receive general error data on DATA_NAMESPACE.

        Args:
            data (Dict[str, Any]): JSON data.
            sid (str, optional): Namespace sid - only on the server side.
        """

        logger.error(f"Data error, eio_sid {self.get_client_eio_sid(sid, DATA_NAMESPACE)}, sid {sid}, data {data}")

    def image_decode(self, data: Dict[str, Any], event: str, sid: Optional[str] = None) -> Optional[Dict]:
        """Decode JPEG or H.264 or HEVC encoded image received on DATA_NAMESPACE.

        Args:
            data (Dict[str, Any]): Received dictionary with frame data.
            event (str): Event name.
            sid (str, optional): Namespace sid - only on the server side.
        """

        if "timestamp" not in data:
            logger.error("Missing timestamp in frame data dictionary.")
            self.send_data(
                {"timestamp": 0, "error": "Missing timestamp in frame data dictionary."},
                self._callbacks_info[event].error_event,
                sid=sid,
            )
            return None
        timestamp = data.get("timestamp", 0)

        if "frame" not in data:
            logger.error("Data does not contain frame.")
            self.send_data(
                {"timestamp": timestamp, "error": "Data does not contain frame."},
                self._callbacks_info[event].error_event,
                sid=sid,
            )
            return None

        eio_sid = self.get_client_eio_sid(sid, DATA_NAMESPACE)
        decoder_id = (eio_sid, event)
        if (
            self._callbacks_info[event].type in (ChannelType.H264, ChannelType.HEVC)
            and decoder_id not in self._decoders
        ):
            if "width" not in data or "height" not in data:
                logger.error("Data does not contain width or height, it is mandatory for video frame decoder.")
                self.send_data(
                    {
                        "timestamp": timestamp,
                        "error": "Data does not contain width or height, it is mandatory for video frame decoder.",
                    },
                    self._callbacks_info[event].error_event,
                    sid=sid,
                )
                return None
            try:
                if self._callbacks_info[event].type is ChannelType.H264:
                    logger.info(f"Creating H.264 decoder for image size {data['width']}x{data['height']}")
                    self._decoders[decoder_id] = FrameDecoder(data["width"], data["height"], codec="h264")
                elif self._callbacks_info[event].type is ChannelType.HEVC:
                    logger.info(f"Creating HEVC decoder for image size {data['width']}x{data['height']}")
                    self._decoders[decoder_id] = FrameDecoder(data["width"], data["height"], codec="hevc")
            except Exception as e:
                logger.error(f"Cannot create video frame decoder: {repr(e)}")
                self.send_data(
                    {"timestamp": timestamp, "error": f"Cannot create video frame decoder: {repr(e)}"},
                    self._callbacks_info[event].error_event,
                    sid=sid,
                )
                return None

        if decoder_id in self._decoders:
            last_timestamp = self._decoders[decoder_id].last_timestamp
            if timestamp - last_timestamp < 0:
                logger.error(
                    f"Received frame with older timestamp: {timestamp}, "
                    f"last_timestamp: {last_timestamp}, diff: {timestamp - last_timestamp}"
                )
                self.send_data(
                    {
                        "timestamp": timestamp,
                        "error": (
                            f"Received frame with older timestamp: {timestamp}, "
                            f"last_timestamp: {last_timestamp}, diff: {timestamp - last_timestamp}"
                        ),
                    },
                    self._callbacks_info[event].error_event,
                    sid=sid,
                )
                return None
            self._decoders[decoder_id].last_timestamp = timestamp

        if decoder_id in self._decoders:
            try:
                frame_decoded = self._decoders[decoder_id].decode_packet_data(data["frame"])
            except FrameDecoderError as e:
                logger.error(f"Video frame decoder error: {e}")
                # Try to recreate decoder
                if self._decoders[decoder_id].get_init_count() < self._recreate_coder_attempts_count:
                    logger.info(f"Try to recreate decoder ... attempt {self._decoders[decoder_id].get_init_count()}")
                    # self._decoders[decoder_id].decoder_init()
                self.send_data(
                    {"timestamp": timestamp, "error": f"Video frame decoder error: {e}"},
                    self._callbacks_info[event].error_event,
                    sid=sid,
                )
                return None
        else:
            try:
                frame_decoded = cv2.imdecode(np.frombuffer(data["frame"], dtype=np.uint8), cv2.IMREAD_COLOR)
            except Exception as e:
                logger.error(f"Failed to decode frame data: {repr(e)}")
                self.send_data(
                    {"timestamp": timestamp, "error": f"Failed to decode frame data: {repr(e)}"},
                    self._callbacks_info[event].error_event,
                    sid=sid,
                )
                return None

        decoded_data = {"frame": frame_decoded, "timestamp": timestamp}
        if "metadata" in data:
            decoded_data["metadata"] = data["metadata"]

        return decoded_data

    def data_lz4_decode(self, data: bytes, event: str, sid: Optional[str] = None) -> Optional[Dict]:
        """Decode LZ4 compressed general JSON data received on DATA_NAMESPACE.

        Args:
            data (bytes): LZ4 compressed JSON data.
            event (str): Event name.
            sid (str, optional): Namespace sid - only on the server side.
        """

        assert isinstance(data, bytes)

        try:
            new_data: Dict = ujson.loads(decompress(data))
            return new_data
        except Exception as e:
            logger.error(f"Failed to decode LZ4 JSON data: {repr(e)}")
            self.send_data(
                {"error": f"Failed to decode LZ4 JSON data: {repr(e)}"},
                self._callbacks_info[event].error_event,
                sid=sid,
            )
            return None

    @property
    def stats(self):
        return self._stats

    @property
    def sizes(self):
        return self._sizes
