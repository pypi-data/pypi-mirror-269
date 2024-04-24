from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

BSENSOR_STATE_EVENT_DETECTED: BinarySensorState
BSENSOR_STATE_IDLE: BinarySensorState
DESCRIPTOR: _descriptor.FileDescriptor
OPEN_CLOSE_STATE_CLOSED: OpenCloseState
OPEN_CLOSE_STATE_OPEN: OpenCloseState

class MotionReport(_message.Message):
    __slots__ = ["state"]
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    DETECTED: MotionReport.State
    IDLE: MotionReport.State
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: MotionReport.State
    def __init__(self, state: _Optional[_Union[MotionReport.State, str]] = ...) -> None: ...

class OpenCloseReport(_message.Message):
    __slots__ = ["state"]
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: OpenCloseState
    def __init__(self, state: _Optional[_Union[OpenCloseState, str]] = ...) -> None: ...

class OpenCloseState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class BinarySensorState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
