from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Status(_message.Message):
    __slots__ = ["firmware_update", "firmware_version", "mac", "wifi_rssi"]
    FIRMWARE_UPDATE_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_VERSION_FIELD_NUMBER: _ClassVar[int]
    MAC_FIELD_NUMBER: _ClassVar[int]
    WIFI_RSSI_FIELD_NUMBER: _ClassVar[int]
    firmware_update: bool
    firmware_version: str
    mac: str
    wifi_rssi: int
    def __init__(self, mac: _Optional[str] = ..., firmware_version: _Optional[str] = ..., firmware_update: bool = ..., wifi_rssi: _Optional[int] = ...) -> None: ...

class StatusCheckReport(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: Status
    def __init__(self, status: _Optional[_Union[Status, _Mapping]] = ...) -> None: ...

class StatusCheckRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class StatusCheckResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
