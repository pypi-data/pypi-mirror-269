from aiovemmio import metadata_pb2 as _metadata_pb2
from aiovemmio import units_pb2 as _units_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

CARBON_MONOXIDE_MAINTENANCE_PERIODIC_INSPECTION: CarbonMonoxideMaintenance
CARBON_MONOXIDE_MAINTENANCE_UNSPECIFIED: CarbonMonoxideMaintenance
CARBON_MONOXIDE_REPLACEMENT_EOL: CarbonMonoxideReplacement
CARBON_MONOXIDE_REPLACEMENT_UNSPECIFIED: CarbonMonoxideReplacement
CARBON_MONOXIDE_STATE_CLEAR: CarbonMonoxideState
CARBON_MONOXIDE_STATE_DETECTED: CarbonMonoxideState
CARBON_MONOXIDE_STATE_MAINTENANCE_REQUIRED: CarbonMonoxideState
CARBON_MONOXIDE_STATE_REPLACEMENT_REQUIRED: CarbonMonoxideState
CARBON_MONOXIDE_STATE_SILENCED: CarbonMonoxideState
CARBON_MONOXIDE_STATE_TEST: CarbonMonoxideState
CARBON_MONOXIDE_STATE_UNSPECIFIED: CarbonMonoxideState
DESCRIPTOR: _descriptor.FileDescriptor

class CarbonMonoxideGetRequest(_message.Message):
    __slots__ = ["metadata"]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: _metadata_pb2.DeviceMetadata
    def __init__(self, metadata: _Optional[_Union[_metadata_pb2.DeviceMetadata, _Mapping]] = ...) -> None: ...

class CarbonMonoxideGetResponse(_message.Message):
    __slots__ = ["unit", "value"]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    unit: _units_pb2.Unit
    value: float
    def __init__(self, unit: _Optional[_Union[_units_pb2.Unit, str]] = ..., value: _Optional[float] = ...) -> None: ...

class CarbonMonoxideStateReport(_message.Message):
    __slots__ = ["maintenance", "replacement", "state"]
    MAINTENANCE_FIELD_NUMBER: _ClassVar[int]
    REPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    maintenance: CarbonMonoxideMaintenance
    replacement: CarbonMonoxideReplacement
    state: CarbonMonoxideState
    def __init__(self, state: _Optional[_Union[CarbonMonoxideState, str]] = ..., replacement: _Optional[_Union[CarbonMonoxideReplacement, str]] = ..., maintenance: _Optional[_Union[CarbonMonoxideMaintenance, str]] = ...) -> None: ...

class CarbonMonoxideValueReport(_message.Message):
    __slots__ = ["unit", "value"]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    unit: _units_pb2.Unit
    value: float
    def __init__(self, unit: _Optional[_Union[_units_pb2.Unit, str]] = ..., value: _Optional[float] = ...) -> None: ...

class CarbonMonoxideState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class CarbonMonoxideReplacement(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class CarbonMonoxideMaintenance(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
