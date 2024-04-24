from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class InfoRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class InfoResponse(_message.Message):
    __slots__ = ["build_time", "common_name", "firmware_version", "git_commit", "version"]
    BUILD_TIME_FIELD_NUMBER: _ClassVar[int]
    COMMON_NAME_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_VERSION_FIELD_NUMBER: _ClassVar[int]
    GIT_COMMIT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    build_time: str
    common_name: str
    firmware_version: str
    git_commit: str
    version: str
    def __init__(self, common_name: _Optional[str] = ..., version: _Optional[str] = ..., git_commit: _Optional[str] = ..., build_time: _Optional[str] = ..., firmware_version: _Optional[str] = ...) -> None: ...
