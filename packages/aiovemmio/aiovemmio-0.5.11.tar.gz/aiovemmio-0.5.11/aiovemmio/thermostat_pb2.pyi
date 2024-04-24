from aiovemmio import metadata_pb2 as _metadata_pb2
from aiovemmio import units_pb2 as _units_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
THERMOSTAT_FAN_MODE_AUTO_HIGH: ThermostatFanMode
THERMOSTAT_FAN_MODE_AUTO_LOW: ThermostatFanMode
THERMOSTAT_FAN_MODE_HIGH: ThermostatFanMode
THERMOSTAT_FAN_MODE_LOW: ThermostatFanMode
THERMOSTAT_FAN_MODE_OFF: ThermostatFanMode
THERMOSTAT_MODE_AUTO: ThermostatMode
THERMOSTAT_MODE_COOL: ThermostatMode
THERMOSTAT_MODE_HEAT: ThermostatMode
THERMOSTAT_MODE_OFF: ThermostatMode
THERMOSTAT_SETPOINT_TYPE_AUTO: ThermostatSetpointType
THERMOSTAT_SETPOINT_TYPE_COOL: ThermostatSetpointType
THERMOSTAT_SETPOINT_TYPE_HEAT: ThermostatSetpointType

class ThermostatFanModeReport(_message.Message):
    __slots__ = ["fan_mode"]
    FAN_MODE_FIELD_NUMBER: _ClassVar[int]
    fan_mode: ThermostatFanMode
    def __init__(self, fan_mode: _Optional[_Union[ThermostatFanMode, str]] = ...) -> None: ...

class ThermostatFanModeSetRequest(_message.Message):
    __slots__ = ["fan_mode", "metadata"]
    FAN_MODE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    fan_mode: ThermostatFanMode
    metadata: _metadata_pb2.DeviceMetadata
    def __init__(self, metadata: _Optional[_Union[_metadata_pb2.DeviceMetadata, _Mapping]] = ..., fan_mode: _Optional[_Union[ThermostatFanMode, str]] = ...) -> None: ...

class ThermostatModeReport(_message.Message):
    __slots__ = ["mode"]
    MODE_FIELD_NUMBER: _ClassVar[int]
    mode: ThermostatMode
    def __init__(self, mode: _Optional[_Union[ThermostatMode, str]] = ...) -> None: ...

class ThermostatModeSetRequest(_message.Message):
    __slots__ = ["metadata", "mode"]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    metadata: _metadata_pb2.DeviceMetadata
    mode: ThermostatMode
    def __init__(self, metadata: _Optional[_Union[_metadata_pb2.DeviceMetadata, _Mapping]] = ..., mode: _Optional[_Union[ThermostatMode, str]] = ...) -> None: ...

class ThermostatModeSupGetRequest(_message.Message):
    __slots__ = ["metadata"]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: _metadata_pb2.DeviceMetadata
    def __init__(self, metadata: _Optional[_Union[_metadata_pb2.DeviceMetadata, _Mapping]] = ...) -> None: ...

class ThermostatModeSupGetResponse(_message.Message):
    __slots__ = ["modes"]
    MODES_FIELD_NUMBER: _ClassVar[int]
    modes: _containers.RepeatedScalarFieldContainer[ThermostatMode]
    def __init__(self, modes: _Optional[_Iterable[_Union[ThermostatMode, str]]] = ...) -> None: ...

class ThermostatResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ThermostatSetpoint(_message.Message):
    __slots__ = ["precision", "unit", "value"]
    PRECISION_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    precision: int
    unit: _units_pb2.Unit
    value: float
    def __init__(self, value: _Optional[float] = ..., unit: _Optional[_Union[_units_pb2.Unit, str]] = ..., precision: _Optional[int] = ...) -> None: ...

class ThermostatSetpointRange(_message.Message):
    __slots__ = ["max", "min", "type"]
    MAX_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    max: ThermostatSetpoint
    min: ThermostatSetpoint
    type: ThermostatSetpointType
    def __init__(self, type: _Optional[_Union[ThermostatSetpointType, str]] = ..., min: _Optional[_Union[ThermostatSetpoint, _Mapping]] = ..., max: _Optional[_Union[ThermostatSetpoint, _Mapping]] = ...) -> None: ...

class ThermostatSetpointReport(_message.Message):
    __slots__ = ["setpoint"]
    SETPOINT_FIELD_NUMBER: _ClassVar[int]
    setpoint: ThermostatSetpoint
    def __init__(self, setpoint: _Optional[_Union[ThermostatSetpoint, _Mapping]] = ...) -> None: ...

class ThermostatSetpointSetRequest(_message.Message):
    __slots__ = ["metadata", "setpoint", "type"]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    SETPOINT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    metadata: _metadata_pb2.DeviceMetadata
    setpoint: ThermostatSetpoint
    type: ThermostatSetpointType
    def __init__(self, metadata: _Optional[_Union[_metadata_pb2.DeviceMetadata, _Mapping]] = ..., type: _Optional[_Union[ThermostatSetpointType, str]] = ..., setpoint: _Optional[_Union[ThermostatSetpoint, _Mapping]] = ...) -> None: ...

class ThermostatMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ThermostatSetpointType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ThermostatFanMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
