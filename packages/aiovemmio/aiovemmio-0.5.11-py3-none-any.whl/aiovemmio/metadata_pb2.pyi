from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddonMetadata(_message.Message):
    __slots__ = ["uuid"]
    UUID_FIELD_NUMBER: _ClassVar[int]
    uuid: str
    def __init__(self, uuid: _Optional[str] = ...) -> None: ...

class AliasMetadata(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DeviceMetadata(_message.Message):
    __slots__ = ["addon", "alias", "mqtt", "zigbee", "zwave"]
    ADDON_FIELD_NUMBER: _ClassVar[int]
    ALIAS_FIELD_NUMBER: _ClassVar[int]
    MQTT_FIELD_NUMBER: _ClassVar[int]
    ZIGBEE_FIELD_NUMBER: _ClassVar[int]
    ZWAVE_FIELD_NUMBER: _ClassVar[int]
    addon: AddonMetadata
    alias: AliasMetadata
    mqtt: MQTTMetadata
    zigbee: ZigbeeMetadata
    zwave: ZWaveMetadata
    def __init__(self, zwave: _Optional[_Union[ZWaveMetadata, _Mapping]] = ..., zigbee: _Optional[_Union[ZigbeeMetadata, _Mapping]] = ..., addon: _Optional[_Union[AddonMetadata, _Mapping]] = ..., alias: _Optional[_Union[AliasMetadata, _Mapping]] = ..., mqtt: _Optional[_Union[MQTTMetadata, _Mapping]] = ...) -> None: ...

class MQTTMetadata(_message.Message):
    __slots__ = ["device_id"]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    device_id: bytes
    def __init__(self, device_id: _Optional[bytes] = ...) -> None: ...

class ZWaveMetadata(_message.Message):
    __slots__ = ["endpoint_id", "node_id"]
    ENDPOINT_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    endpoint_id: int
    node_id: int
    def __init__(self, node_id: _Optional[int] = ..., endpoint_id: _Optional[int] = ...) -> None: ...

class ZigbeeMetadata(_message.Message):
    __slots__ = ["endpoint", "eui64_addr"]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    EUI64_ADDR_FIELD_NUMBER: _ClassVar[int]
    endpoint: int
    eui64_addr: str
    def __init__(self, eui64_addr: _Optional[str] = ..., endpoint: _Optional[int] = ...) -> None: ...
