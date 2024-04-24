from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

CARBON_DIOXIDE_MAINTENANCE_PERIODIC_INSPECTION: CarbonDioxideMaintenance
CARBON_DIOXIDE_MAINTENANCE_UNSPECIFIED: CarbonDioxideMaintenance
CARBON_DIOXIDE_REPLACEMENT_EOL: CarbonDioxideReplacement
CARBON_DIOXIDE_REPLACEMENT_UNSPECIFIED: CarbonDioxideReplacement
CARBON_DIOXIDE_STATE_CLEAR: CarbonDioxideState
CARBON_DIOXIDE_STATE_DETECTED: CarbonDioxideState
CARBON_DIOXIDE_STATE_MAINTENANCE_REQUIRED: CarbonDioxideState
CARBON_DIOXIDE_STATE_REPLACEMENT_REQUIRED: CarbonDioxideState
CARBON_DIOXIDE_STATE_SILENCED: CarbonDioxideState
CARBON_DIOXIDE_STATE_TEST: CarbonDioxideState
CARBON_DIOXIDE_STATE_UNSPECIFIED: CarbonDioxideState
DESCRIPTOR: _descriptor.FileDescriptor

class CarbonDioxideReport(_message.Message):
    __slots__ = ["maintenance", "replacement", "state"]
    MAINTENANCE_FIELD_NUMBER: _ClassVar[int]
    REPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    maintenance: CarbonDioxideMaintenance
    replacement: CarbonDioxideReplacement
    state: CarbonDioxideState
    def __init__(self, state: _Optional[_Union[CarbonDioxideState, str]] = ..., replacement: _Optional[_Union[CarbonDioxideReplacement, str]] = ..., maintenance: _Optional[_Union[CarbonDioxideMaintenance, str]] = ...) -> None: ...

class CarbonDioxideState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class CarbonDioxideReplacement(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class CarbonDioxideMaintenance(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
