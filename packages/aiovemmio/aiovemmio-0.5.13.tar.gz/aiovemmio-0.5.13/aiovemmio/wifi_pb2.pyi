from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WiFiBSS(_message.Message):
    __slots__ = ["frequency", "last_seen", "ssid"]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    LAST_SEEN_FIELD_NUMBER: _ClassVar[int]
    SSID_FIELD_NUMBER: _ClassVar[int]
    frequency: int
    last_seen: int
    ssid: str
    def __init__(self, ssid: _Optional[str] = ..., frequency: _Optional[int] = ..., last_seen: _Optional[int] = ...) -> None: ...

class WiFiConnectRequest(_message.Message):
    __slots__ = ["psk", "ssid"]
    PSK_FIELD_NUMBER: _ClassVar[int]
    SSID_FIELD_NUMBER: _ClassVar[int]
    psk: str
    ssid: str
    def __init__(self, ssid: _Optional[str] = ..., psk: _Optional[str] = ...) -> None: ...

class WiFiConnectResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class WiFiInterface(_message.Message):
    __slots__ = ["bss", "hardware_addr", "name", "stations"]
    BSS_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_ADDR_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATIONS_FIELD_NUMBER: _ClassVar[int]
    bss: WiFiBSS
    hardware_addr: bytes
    name: str
    stations: _containers.RepeatedCompositeFieldContainer[WiFiStation]
    def __init__(self, name: _Optional[str] = ..., hardware_addr: _Optional[bytes] = ..., bss: _Optional[_Union[WiFiBSS, _Mapping]] = ..., stations: _Optional[_Iterable[_Union[WiFiStation, _Mapping]]] = ...) -> None: ...

class WiFiQueryRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class WiFiQueryResponse(_message.Message):
    __slots__ = ["interfaces", "timestamp"]
    INTERFACES_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    interfaces: _containers.RepeatedCompositeFieldContainer[WiFiInterface]
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, interfaces: _Optional[_Iterable[_Union[WiFiInterface, _Mapping]]] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class WiFiScanRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class WiFiScanResponse(_message.Message):
    __slots__ = ["bsss"]
    BSSS_FIELD_NUMBER: _ClassVar[int]
    bsss: _containers.RepeatedCompositeFieldContainer[WiFiBSS]
    def __init__(self, bsss: _Optional[_Iterable[_Union[WiFiBSS, _Mapping]]] = ...) -> None: ...

class WiFiStation(_message.Message):
    __slots__ = ["connected", "hardware_addr", "inactive", "signal"]
    CONNECTED_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_ADDR_FIELD_NUMBER: _ClassVar[int]
    INACTIVE_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_FIELD_NUMBER: _ClassVar[int]
    connected: int
    hardware_addr: bytes
    inactive: int
    signal: int
    def __init__(self, hardware_addr: _Optional[bytes] = ..., signal: _Optional[int] = ..., connected: _Optional[int] = ..., inactive: _Optional[int] = ...) -> None: ...
