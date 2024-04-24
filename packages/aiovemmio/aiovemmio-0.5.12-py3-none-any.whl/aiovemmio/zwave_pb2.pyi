from google.protobuf import wrappers_pb2 as _wrappers_pb2
from aiovemmio import devices_pb2 as _devices_pb2
from aiovemmio import metadata_pb2 as _metadata_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
NODE_STATUS_ALIVE: ZWaveNodeStatus
NODE_STATUS_DOWN: ZWaveNodeStatus
NODE_STATUS_SLEEP: ZWaveNodeStatus
NODE_STATUS_UNSPECIFIED: ZWaveNodeStatus
ZWAVE_HEALTH_CRITICAL: ZWaveHealthCategory
ZWAVE_HEALTH_GREEN: ZWaveHealthCategory
ZWAVE_HEALTH_RED: ZWaveHealthCategory
ZWAVE_HEALTH_UNSPECIFIED: ZWaveHealthCategory
ZWAVE_HEALTH_YELLOW: ZWaveHealthCategory

class ZWaveAbortRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveAbortResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveAddEntryRequest(_message.Message):
    __slots__ = ["dsk", "info"]
    DSK_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    dsk: str
    info: _containers.RepeatedCompositeFieldContainer[ZWaveProvisioningInfo]
    def __init__(self, dsk: _Optional[str] = ..., info: _Optional[_Iterable[_Union[ZWaveProvisioningInfo, _Mapping]]] = ...) -> None: ...

class ZWaveAddEntryResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveEndpoint(_message.Message):
    __slots__ = ["ep_id", "generic_class", "interfaces", "specific_class"]
    EP_ID_FIELD_NUMBER: _ClassVar[int]
    GENERIC_CLASS_FIELD_NUMBER: _ClassVar[int]
    INTERFACES_FIELD_NUMBER: _ClassVar[int]
    SPECIFIC_CLASS_FIELD_NUMBER: _ClassVar[int]
    ep_id: int
    generic_class: int
    interfaces: _containers.RepeatedCompositeFieldContainer[ZWaveInterface]
    specific_class: int
    def __init__(self, ep_id: _Optional[int] = ..., generic_class: _Optional[int] = ..., specific_class: _Optional[int] = ..., interfaces: _Optional[_Iterable[_Union[ZWaveInterface, _Mapping]]] = ...) -> None: ...

class ZWaveExcludeRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveExcludeStatus(_message.Message):
    __slots__ = ["not_found", "progress", "ready", "removed"]
    class DeviceNotFound(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    class DeviceRemoved(_message.Message):
        __slots__ = ["metadata"]
        METADATA_FIELD_NUMBER: _ClassVar[int]
        metadata: _metadata_pb2.ZWaveMetadata
        def __init__(self, metadata: _Optional[_Union[_metadata_pb2.ZWaveMetadata, _Mapping]] = ...) -> None: ...
    class ExcludeProgress(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    class ExcludeReady(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    NOT_FOUND_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    not_found: ZWaveExcludeStatus.DeviceNotFound
    progress: ZWaveExcludeStatus.ExcludeProgress
    ready: ZWaveExcludeStatus.ExcludeReady
    removed: ZWaveExcludeStatus.DeviceRemoved
    def __init__(self, removed: _Optional[_Union[ZWaveExcludeStatus.DeviceRemoved, _Mapping]] = ..., ready: _Optional[_Union[ZWaveExcludeStatus.ExcludeReady, _Mapping]] = ..., progress: _Optional[_Union[ZWaveExcludeStatus.ExcludeProgress, _Mapping]] = ..., not_found: _Optional[_Union[ZWaveExcludeStatus.DeviceNotFound, _Mapping]] = ...) -> None: ...

class ZWaveHealRequest(_message.Message):
    __slots__ = ["init_return_routes", "node_id"]
    INIT_RETURN_ROUTES_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    init_return_routes: bool
    node_id: _wrappers_pb2.Int32Value
    def __init__(self, node_id: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., init_return_routes: bool = ...) -> None: ...

class ZWaveHealResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveHealthCheckCompleted(_message.Message):
    __slots__ = ["nodes"]
    NODES_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[ZWaveHealthStatusNode]
    def __init__(self, nodes: _Optional[_Iterable[_Union[ZWaveHealthStatusNode, _Mapping]]] = ...) -> None: ...

class ZWaveHealthCheckProgress(_message.Message):
    __slots__ = ["count", "total"]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    count: int
    total: int
    def __init__(self, count: _Optional[int] = ..., total: _Optional[int] = ...) -> None: ...

class ZWaveHealthCheckRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveHealthCheckStarted(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveHealthCheckStatus(_message.Message):
    __slots__ = ["completed", "progress", "started"]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    STARTED_FIELD_NUMBER: _ClassVar[int]
    completed: ZWaveHealthCheckCompleted
    progress: ZWaveHealthCheckProgress
    started: ZWaveHealthCheckStarted
    def __init__(self, started: _Optional[_Union[ZWaveHealthCheckStarted, _Mapping]] = ..., progress: _Optional[_Union[ZWaveHealthCheckProgress, _Mapping]] = ..., completed: _Optional[_Union[ZWaveHealthCheckCompleted, _Mapping]] = ...) -> None: ...

class ZWaveHealthStatusNode(_message.Message):
    __slots__ = ["category", "node_id", "value"]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    category: ZWaveHealthCategory
    node_id: int
    value: int
    def __init__(self, node_id: _Optional[int] = ..., category: _Optional[_Union[ZWaveHealthCategory, str]] = ..., value: _Optional[int] = ...) -> None: ...

class ZWaveIncludeRequest(_message.Message):
    __slots__ = ["secure"]
    SECURE_FIELD_NUMBER: _ClassVar[int]
    secure: bool
    def __init__(self, secure: bool = ...) -> None: ...

class ZWaveIncludeStatus(_message.Message):
    __slots__ = ["added", "found", "progress", "ready"]
    class DeviceAdded(_message.Message):
        __slots__ = ["devices"]
        DEVICES_FIELD_NUMBER: _ClassVar[int]
        devices: _containers.RepeatedCompositeFieldContainer[_devices_pb2.Device]
        def __init__(self, devices: _Optional[_Iterable[_Union[_devices_pb2.Device, _Mapping]]] = ...) -> None: ...
    class DeviceFound(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    class IncludeProgress(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    class IncludeReady(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    ADDED_FIELD_NUMBER: _ClassVar[int]
    FOUND_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    added: ZWaveIncludeStatus.DeviceAdded
    found: ZWaveIncludeStatus.DeviceFound
    progress: ZWaveIncludeStatus.IncludeProgress
    ready: ZWaveIncludeStatus.IncludeReady
    def __init__(self, found: _Optional[_Union[ZWaveIncludeStatus.DeviceFound, _Mapping]] = ..., added: _Optional[_Union[ZWaveIncludeStatus.DeviceAdded, _Mapping]] = ..., ready: _Optional[_Union[ZWaveIncludeStatus.IncludeReady, _Mapping]] = ..., progress: _Optional[_Union[ZWaveIncludeStatus.IncludeProgress, _Mapping]] = ...) -> None: ...

class ZWaveInterface(_message.Message):
    __slots__ = ["command_class", "help", "items", "label", "real_version", "version"]
    COMMAND_CLASS_FIELD_NUMBER: _ClassVar[int]
    HELP_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    REAL_VERSION_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    command_class: int
    help: str
    items: _containers.RepeatedCompositeFieldContainer[ZWaveValueItem]
    label: str
    real_version: int
    version: int
    def __init__(self, command_class: _Optional[int] = ..., version: _Optional[int] = ..., real_version: _Optional[int] = ..., label: _Optional[str] = ..., help: _Optional[str] = ..., items: _Optional[_Iterable[_Union[ZWaveValueItem, _Mapping]]] = ...) -> None: ...

class ZWaveListEntriesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveListEntriesResponse(_message.Message):
    __slots__ = ["entries"]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedCompositeFieldContainer[ZWaveProvisioningEntry]
    def __init__(self, entries: _Optional[_Iterable[_Union[ZWaveProvisioningEntry, _Mapping]]] = ...) -> None: ...

class ZWaveNetworkTopologyUpdateStarted(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveNode(_message.Message):
    __slots__ = ["endpoints", "manufacturer_name", "node_id", "product_id", "product_name", "product_type", "status", "user_name", "vendor_id"]
    ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    MANUFACTURER_NAME_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_NAME_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_TYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    USER_NAME_FIELD_NUMBER: _ClassVar[int]
    VENDOR_ID_FIELD_NUMBER: _ClassVar[int]
    endpoints: _containers.RepeatedCompositeFieldContainer[ZWaveEndpoint]
    manufacturer_name: str
    node_id: int
    product_id: int
    product_name: str
    product_type: int
    status: ZWaveNodeStatus
    user_name: str
    vendor_id: int
    def __init__(self, node_id: _Optional[int] = ..., vendor_id: _Optional[int] = ..., product_type: _Optional[int] = ..., product_id: _Optional[int] = ..., endpoints: _Optional[_Iterable[_Union[ZWaveEndpoint, _Mapping]]] = ..., manufacturer_name: _Optional[str] = ..., product_name: _Optional[str] = ..., user_name: _Optional[str] = ..., status: _Optional[_Union[ZWaveNodeStatus, str]] = ...) -> None: ...

class ZWaveNodeInformationUpdateStarted(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveNodeNeighborUpdateStarted(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveNodeRequest(_message.Message):
    __slots__ = ["node_id"]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    def __init__(self, node_id: _Optional[int] = ...) -> None: ...

class ZWaveNodeResponse(_message.Message):
    __slots__ = ["node"]
    NODE_FIELD_NUMBER: _ClassVar[int]
    node: ZWaveNode
    def __init__(self, node: _Optional[_Union[ZWaveNode, _Mapping]] = ...) -> None: ...

class ZWaveNodesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveNodesResponse(_message.Message):
    __slots__ = ["nodes"]
    NODES_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[ZWaveNode]
    def __init__(self, nodes: _Optional[_Iterable[_Union[ZWaveNode, _Mapping]]] = ...) -> None: ...

class ZWaveNotificationItemsRequest(_message.Message):
    __slots__ = ["ep_id", "index", "node_id"]
    EP_ID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    ep_id: int
    index: int
    node_id: int
    def __init__(self, node_id: _Optional[int] = ..., ep_id: _Optional[int] = ..., index: _Optional[int] = ...) -> None: ...

class ZWaveNotificationItemsResponse(_message.Message):
    __slots__ = ["items"]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, items: _Optional[_Iterable[int]] = ...) -> None: ...

class ZWaveProvisioningEntry(_message.Message):
    __slots__ = ["dsk", "info"]
    DSK_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    dsk: str
    info: _containers.RepeatedCompositeFieldContainer[ZWaveProvisioningInfo]
    def __init__(self, dsk: _Optional[str] = ..., info: _Optional[_Iterable[_Union[ZWaveProvisioningInfo, _Mapping]]] = ...) -> None: ...

class ZWaveProvisioningInfo(_message.Message):
    __slots__ = ["bootstrapping_mode", "granted_keys", "inclusion_interval", "inclusion_status", "location", "name", "network_status", "product_id", "product_type", "uuid"]
    BOOTSTRAPPING_MODE_FIELD_NUMBER: _ClassVar[int]
    GRANTED_KEYS_FIELD_NUMBER: _ClassVar[int]
    INCLUSION_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    INCLUSION_STATUS_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NETWORK_STATUS_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_TYPE_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    bootstrapping_mode: int
    granted_keys: int
    inclusion_interval: int
    inclusion_status: int
    location: str
    name: str
    network_status: ZWaveProvisioningInfoNetworkStatus
    product_id: ZWaveProvisioningInfoProductID
    product_type: ZWaveProvisioningInfoProductType
    uuid: str
    def __init__(self, product_type: _Optional[_Union[ZWaveProvisioningInfoProductType, _Mapping]] = ..., product_id: _Optional[_Union[ZWaveProvisioningInfoProductID, _Mapping]] = ..., inclusion_interval: _Optional[int] = ..., uuid: _Optional[str] = ..., name: _Optional[str] = ..., location: _Optional[str] = ..., inclusion_status: _Optional[int] = ..., granted_keys: _Optional[int] = ..., bootstrapping_mode: _Optional[int] = ..., network_status: _Optional[_Union[ZWaveProvisioningInfoNetworkStatus, _Mapping]] = ...) -> None: ...

class ZWaveProvisioningInfoNetworkStatus(_message.Message):
    __slots__ = ["node_id", "status"]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    status: int
    def __init__(self, node_id: _Optional[int] = ..., status: _Optional[int] = ...) -> None: ...

class ZWaveProvisioningInfoProductID(_message.Message):
    __slots__ = ["application_sub_version", "application_version", "manufacturer_id", "product_id", "product_type"]
    APPLICATION_SUB_VERSION_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_VERSION_FIELD_NUMBER: _ClassVar[int]
    MANUFACTURER_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    PRODUCT_TYPE_FIELD_NUMBER: _ClassVar[int]
    application_sub_version: int
    application_version: int
    manufacturer_id: int
    product_id: int
    product_type: int
    def __init__(self, manufacturer_id: _Optional[int] = ..., product_type: _Optional[int] = ..., product_id: _Optional[int] = ..., application_version: _Optional[int] = ..., application_sub_version: _Optional[int] = ...) -> None: ...

class ZWaveProvisioningInfoProductType(_message.Message):
    __slots__ = ["generic_class", "icon_type", "specific_class"]
    GENERIC_CLASS_FIELD_NUMBER: _ClassVar[int]
    ICON_TYPE_FIELD_NUMBER: _ClassVar[int]
    SPECIFIC_CLASS_FIELD_NUMBER: _ClassVar[int]
    generic_class: int
    icon_type: int
    specific_class: int
    def __init__(self, generic_class: _Optional[int] = ..., specific_class: _Optional[int] = ..., icon_type: _Optional[int] = ...) -> None: ...

class ZWaveRemoveEntryRequest(_message.Message):
    __slots__ = ["dsk"]
    DSK_FIELD_NUMBER: _ClassVar[int]
    dsk: str
    def __init__(self, dsk: _Optional[str] = ...) -> None: ...

class ZWaveRemoveEntryResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveRemoveFailedRequest(_message.Message):
    __slots__ = ["node_id"]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    def __init__(self, node_id: _Optional[int] = ...) -> None: ...

class ZWaveRemoveFailedResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveReplaceFailedRequest(_message.Message):
    __slots__ = ["node_id"]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    def __init__(self, node_id: _Optional[int] = ...) -> None: ...

class ZWaveReplaceFailedResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveResetRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveResetResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveTestRequest(_message.Message):
    __slots__ = ["count", "node_id"]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    count: int
    node_id: _wrappers_pb2.Int32Value
    def __init__(self, node_id: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., count: _Optional[int] = ...) -> None: ...

class ZWaveTestResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveUpdateNodeRequest(_message.Message):
    __slots__ = ["node_id"]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    def __init__(self, node_id: _Optional[int] = ...) -> None: ...

class ZWaveUpdateNodeResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveUpdateRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ZWaveUpdateStatus(_message.Message):
    __slots__ = ["neighbor", "node_info", "topology"]
    NEIGHBOR_FIELD_NUMBER: _ClassVar[int]
    NODE_INFO_FIELD_NUMBER: _ClassVar[int]
    TOPOLOGY_FIELD_NUMBER: _ClassVar[int]
    neighbor: ZWaveNodeNeighborUpdateStarted
    node_info: ZWaveNodeInformationUpdateStarted
    topology: ZWaveNetworkTopologyUpdateStarted
    def __init__(self, topology: _Optional[_Union[ZWaveNetworkTopologyUpdateStarted, _Mapping]] = ..., neighbor: _Optional[_Union[ZWaveNodeNeighborUpdateStarted, _Mapping]] = ..., node_info: _Optional[_Union[ZWaveNodeInformationUpdateStarted, _Mapping]] = ...) -> None: ...

class ZWaveValueItem(_message.Message):
    __slots__ = ["label", "value"]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    label: str
    value: int
    def __init__(self, value: _Optional[int] = ..., label: _Optional[str] = ...) -> None: ...

class ZWaveHealthCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ZWaveNodeStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
