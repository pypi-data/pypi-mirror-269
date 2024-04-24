from aiovemmio import metadata_pb2 as _metadata_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
GATE_CLOSED: GateState
GATE_CYCLED: GateState
GATE_OPENED: GateState
GATE_UNKNOWN: GateState

class GateReport(_message.Message):
    __slots__ = ["state"]
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: GateState
    def __init__(self, state: _Optional[_Union[GateState, str]] = ...) -> None: ...

class GateRequest(_message.Message):
    __slots__ = ["metadata"]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: _metadata_pb2.DeviceMetadata
    def __init__(self, metadata: _Optional[_Union[_metadata_pb2.DeviceMetadata, _Mapping]] = ...) -> None: ...

class GateResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GateState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
