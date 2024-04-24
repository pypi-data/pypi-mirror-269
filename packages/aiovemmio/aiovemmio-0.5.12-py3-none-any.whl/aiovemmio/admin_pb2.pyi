from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LogsChunk(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class LogsRequest(_message.Message):
    __slots__ = ["count", "filter"]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    count: int
    filter: str
    def __init__(self, filter: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class WalkNodesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class WalkNodesResponse(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...
