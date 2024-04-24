from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

AC_POWER_LOST: PowerSourceEvent
AC_POWER_RESTORED: PowerSourceEvent
BATTERY_CHARGED: PowerSourceEvent
BATTERY_CHARGING: PowerSourceEvent
BATTERY_CRITICAL: PowerSourceEvent
BATTERY_LOW: PowerSourceEvent
BATTERY_REPLACE_NOW: PowerSourceEvent
BATTERY_REPLACE_SOON: PowerSourceEvent
BROWNOUT_DETECTED: PowerSourceEvent
CLEAR: PowerSourceEvent
DESCRIPTOR: _descriptor.FileDescriptor
LOAD_ERROR: PowerSourceEvent
OVER_CURRENT_DETECTED: PowerSourceEvent
OVER_LOAD_DETECTED: PowerSourceEvent
OVER_VOLTAGE_DETECTED: PowerSourceEvent
POWER_APPLIED: PowerSourceEvent
SURGE_DETECTED: PowerSourceEvent

class PowerSourceReport(_message.Message):
    __slots__ = ["event"]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    event: PowerSourceEvent
    def __init__(self, event: _Optional[_Union[PowerSourceEvent, str]] = ...) -> None: ...

class PowerSourceEvent(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
