"""
maix.rtsp module
"""
from __future__ import annotations
import maix._maix.camera
import maix._maix.err
import typing
__all__ = ['Rtsp', 'RtspStreamType']
class Rtsp:
    def __init__(self, ip: str = '', port: int = 8554, fps: int = 30, stream_type: RtspStreamType = ...) -> None:
        ...
    def bind_camera(self, camera: maix._maix.camera.Camera) -> maix._maix.err.Err:
        """
        Bind camera
        
        Args:
          - camera: camera object
        
        
        Returns: error code, err::ERR_NONE means success, others means failed
        """
    def get_url(self) -> str:
        """
        Get url of rtsp
        
        Returns: url of rtsp
        """
    def rtsp_is_start(self) -> bool:
        """
        return rtsp start status
        
        Returns: true means rtsp is start, false means rtsp is stop.
        """
    def start(self) -> maix._maix.err.Err:
        """
        start rtsp
        
        Returns: error code, err::ERR_NONE means success, others means failed
        """
    def to_camera(self) -> maix._maix.camera.Camera:
        """
        Get camera object from rtsp
        
        Returns: camera object
        """
    def write(self, stream: ...) -> maix._maix.err.Err:
        """
        Write data to rtsp
        
        Args:
          - type: rtsp stream type
          - data: rtsp stream data
          - fps: rtsp stream data size
        
        
        Returns: error code, err::ERR_NONE means success, others means failed
        """
class RtspStreamType:
    """
    Members:
    
      RTSP_STREAM_NONE
    
      RTSP_STREAM_H265
    """
    RTSP_STREAM_H265: typing.ClassVar[RtspStreamType]  # value = <RtspStreamType.RTSP_STREAM_H265: 1>
    RTSP_STREAM_NONE: typing.ClassVar[RtspStreamType]  # value = <RtspStreamType.RTSP_STREAM_NONE: 0>
    __members__: typing.ClassVar[dict[str, RtspStreamType]]  # value = {'RTSP_STREAM_NONE': <RtspStreamType.RTSP_STREAM_NONE: 0>, 'RTSP_STREAM_H265': <RtspStreamType.RTSP_STREAM_H265: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
