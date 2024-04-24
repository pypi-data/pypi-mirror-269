from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
EMERGENCY_FIRE: EmergencyType
EMERGENCY_MEDICAL: EmergencyType
EMERGENCY_POLICE: EmergencyType

class EmergencyReport(_message.Message):
    __slots__ = ["type"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: EmergencyType
    def __init__(self, type: _Optional[_Union[EmergencyType, str]] = ...) -> None: ...

class EmergencyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
