from aiovemmio import metadata_pb2 as _metadata_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

CONFIGURATION_VALUE_TYPE_BOOL: ConfigurationValueType
CONFIGURATION_VALUE_TYPE_FLOAT32: ConfigurationValueType
CONFIGURATION_VALUE_TYPE_FLOAT64: ConfigurationValueType
CONFIGURATION_VALUE_TYPE_INT16: ConfigurationValueType
CONFIGURATION_VALUE_TYPE_INT32: ConfigurationValueType
CONFIGURATION_VALUE_TYPE_INT64: ConfigurationValueType
CONFIGURATION_VALUE_TYPE_INT8: ConfigurationValueType
CONFIGURATION_VALUE_TYPE_STRING: ConfigurationValueType
CONFIGURATION_VALUE_TYPE_UINT16: ConfigurationValueType
CONFIGURATION_VALUE_TYPE_UINT32: ConfigurationValueType
CONFIGURATION_VALUE_TYPE_UINT64: ConfigurationValueType
CONFIGURATION_VALUE_TYPE_UINT8: ConfigurationValueType
CONFIGURATION_VALUE_TYPE_UNDEFINED: ConfigurationValueType
DESCRIPTOR: _descriptor.FileDescriptor

class ConfigurationGetRequest(_message.Message):
    __slots__ = ["index", "metadata"]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    index: int
    metadata: _metadata_pb2.DeviceMetadata
    def __init__(self, metadata: _Optional[_Union[_metadata_pb2.DeviceMetadata, _Mapping]] = ..., index: _Optional[int] = ...) -> None: ...

class ConfigurationGetResponse(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: ConfigurationValue
    def __init__(self, value: _Optional[_Union[ConfigurationValue, _Mapping]] = ...) -> None: ...

class ConfigurationListRequest(_message.Message):
    __slots__ = ["metadata"]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: _metadata_pb2.DeviceMetadata
    def __init__(self, metadata: _Optional[_Union[_metadata_pb2.DeviceMetadata, _Mapping]] = ...) -> None: ...

class ConfigurationListResponse(_message.Message):
    __slots__ = ["options"]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    options: _containers.RepeatedCompositeFieldContainer[ConfigurationOption]
    def __init__(self, options: _Optional[_Iterable[_Union[ConfigurationOption, _Mapping]]] = ...) -> None: ...

class ConfigurationOption(_message.Message):
    __slots__ = ["help", "index", "label", "type"]
    HELP_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    help: str
    index: int
    label: str
    type: ConfigurationValueType
    def __init__(self, index: _Optional[int] = ..., label: _Optional[str] = ..., help: _Optional[str] = ..., type: _Optional[_Union[ConfigurationValueType, str]] = ...) -> None: ...

class ConfigurationSetRequest(_message.Message):
    __slots__ = ["index", "metadata", "value"]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    index: int
    metadata: _metadata_pb2.DeviceMetadata
    value: ConfigurationValue
    def __init__(self, metadata: _Optional[_Union[_metadata_pb2.DeviceMetadata, _Mapping]] = ..., index: _Optional[int] = ..., value: _Optional[_Union[ConfigurationValue, _Mapping]] = ...) -> None: ...

class ConfigurationSetResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ConfigurationValue(_message.Message):
    __slots__ = ["scalar"]
    SCALAR_FIELD_NUMBER: _ClassVar[int]
    scalar: ConfigurationValueScalar
    def __init__(self, scalar: _Optional[_Union[ConfigurationValueScalar, _Mapping]] = ...) -> None: ...

class ConfigurationValueScalar(_message.Message):
    __slots__ = ["bool_value", "float32_value", "float64_value", "int16_value", "int32_value", "int64_value", "int8_value", "string_value", "uint16_value", "uint32_value", "uint64_value", "uint8_value"]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    FLOAT32_VALUE_FIELD_NUMBER: _ClassVar[int]
    FLOAT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT16_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT32_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT8_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    UINT16_VALUE_FIELD_NUMBER: _ClassVar[int]
    UINT32_VALUE_FIELD_NUMBER: _ClassVar[int]
    UINT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    UINT8_VALUE_FIELD_NUMBER: _ClassVar[int]
    bool_value: bool
    float32_value: float
    float64_value: float
    int16_value: int
    int32_value: int
    int64_value: int
    int8_value: int
    string_value: str
    uint16_value: int
    uint32_value: int
    uint64_value: int
    uint8_value: int
    def __init__(self, bool_value: bool = ..., uint8_value: _Optional[int] = ..., uint16_value: _Optional[int] = ..., uint32_value: _Optional[int] = ..., uint64_value: _Optional[int] = ..., int8_value: _Optional[int] = ..., int16_value: _Optional[int] = ..., int32_value: _Optional[int] = ..., int64_value: _Optional[int] = ..., float32_value: _Optional[float] = ..., float64_value: _Optional[float] = ..., string_value: _Optional[str] = ...) -> None: ...

class ConfigurationValueType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
