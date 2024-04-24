from aiovemmio import metadata_pb2 as _metadata_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RemoteReport(_message.Message):
    __slots__ = ["count", "event", "key"]
    class Event(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    COUNT_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    HELD_DOWN: RemoteReport.Event
    KEY_FIELD_NUMBER: _ClassVar[int]
    PRESSED: RemoteReport.Event
    RELEASED: RemoteReport.Event
    UNKNOWN: RemoteReport.Event
    count: int
    event: RemoteReport.Event
    key: int
    def __init__(self, event: _Optional[_Union[RemoteReport.Event, str]] = ..., count: _Optional[int] = ..., key: _Optional[int] = ...) -> None: ...

class RemoteRequest(_message.Message):
    __slots__ = ["key", "metadata"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    key: int
    metadata: _metadata_pb2.DeviceMetadata
    def __init__(self, metadata: _Optional[_Union[_metadata_pb2.DeviceMetadata, _Mapping]] = ..., key: _Optional[int] = ...) -> None: ...

class RemoteResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
