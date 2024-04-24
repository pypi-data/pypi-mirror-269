from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
SMOKE_MAINTENANCE_DUST_IN_DEVICE: SmokeDetectorMaintenance
SMOKE_MAINTENANCE_PERIODIC_INSPECTION: SmokeDetectorMaintenance
SMOKE_MAINTENANCE_UNSPECIFIED: SmokeDetectorMaintenance
SMOKE_REPLACEMENT_EOL: SmokeDetectorReplacement
SMOKE_REPLACEMENT_UNSPECIFIED: SmokeDetectorReplacement
SMOKE_STATE_CLEAR: SmokeDetectorState
SMOKE_STATE_DETECTED: SmokeDetectorState
SMOKE_STATE_MAINTENANCE_REQUIRED: SmokeDetectorState
SMOKE_STATE_REPLACEMENT_REQUIRED: SmokeDetectorState
SMOKE_STATE_SILENCED: SmokeDetectorState
SMOKE_STATE_TEST: SmokeDetectorState
SMOKE_STATE_UNSPECIFIED: SmokeDetectorState

class SmokeReport(_message.Message):
    __slots__ = ["maintenance", "replacement", "state"]
    MAINTENANCE_FIELD_NUMBER: _ClassVar[int]
    REPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    maintenance: SmokeDetectorMaintenance
    replacement: SmokeDetectorReplacement
    state: SmokeDetectorState
    def __init__(self, state: _Optional[_Union[SmokeDetectorState, str]] = ..., replacement: _Optional[_Union[SmokeDetectorReplacement, str]] = ..., maintenance: _Optional[_Union[SmokeDetectorMaintenance, str]] = ...) -> None: ...

class SmokeDetectorState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class SmokeDetectorReplacement(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class SmokeDetectorMaintenance(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
