from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MetricType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    UNKNOWN: _ClassVar[MetricType]
    INTEGER: _ClassVar[MetricType]
    DECIMAL: _ClassVar[MetricType]
    TEXT: _ClassVar[MetricType]
    DATE: _ClassVar[MetricType]
    TRUTH: _ClassVar[MetricType]
    URL: _ClassVar[MetricType]

class OperationEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    GET: _ClassVar[OperationEnum]
    CREATE: _ClassVar[OperationEnum]
    READ: _ClassVar[OperationEnum]
    UPDATE: _ClassVar[OperationEnum]
    DELETE: _ClassVar[OperationEnum]
    MATCHING: _ClassVar[OperationEnum]
    BULK_CREATE: _ClassVar[OperationEnum]
    AVAILABLE_METRICS: _ClassVar[OperationEnum]
UNKNOWN: MetricType
INTEGER: MetricType
DECIMAL: MetricType
TEXT: MetricType
DATE: MetricType
TRUTH: MetricType
URL: MetricType
GET: OperationEnum
CREATE: OperationEnum
READ: OperationEnum
UPDATE: OperationEnum
DELETE: OperationEnum
MATCHING: OperationEnum
BULK_CREATE: OperationEnum
AVAILABLE_METRICS: OperationEnum

class MetricMatchingObject(_message.Message):
    __slots__ = ["metric_uuid", "match_to_metric_uuid"]
    METRIC_UUID_FIELD_NUMBER: _ClassVar[int]
    MATCH_TO_METRIC_UUID_FIELD_NUMBER: _ClassVar[int]
    metric_uuid: str
    match_to_metric_uuid: str
    def __init__(self, metric_uuid: _Optional[str] = ..., match_to_metric_uuid: _Optional[str] = ...) -> None: ...

class MetricsMatchingRequest(_message.Message):
    __slots__ = ["metrics", "connect_portal_uuid"]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    CONNECT_PORTAL_UUID_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[MetricMatchingObject]
    connect_portal_uuid: str
    def __init__(self, metrics: _Optional[_Iterable[_Union[MetricMatchingObject, _Mapping]]] = ..., connect_portal_uuid: _Optional[str] = ...) -> None: ...

class MetricReadRequest(_message.Message):
    __slots__ = ["company_uuid"]
    COMPANY_UUID_FIELD_NUMBER: _ClassVar[int]
    company_uuid: str
    def __init__(self, company_uuid: _Optional[str] = ...) -> None: ...

class MetricGetRequest(_message.Message):
    __slots__ = ["metric_uuid"]
    METRIC_UUID_FIELD_NUMBER: _ClassVar[int]
    metric_uuid: str
    def __init__(self, metric_uuid: _Optional[str] = ...) -> None: ...

class MetricCreateRequest(_message.Message):
    __slots__ = ["connect_portal_uuid", "company_uuid", "key", "name", "custom", "connect_portal_method", "type", "configuration", "connected_metrics"]
    CONNECT_PORTAL_UUID_FIELD_NUMBER: _ClassVar[int]
    COMPANY_UUID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIELD_NUMBER: _ClassVar[int]
    CONNECT_PORTAL_METHOD_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_METRICS_FIELD_NUMBER: _ClassVar[int]
    connect_portal_uuid: str
    company_uuid: str
    key: str
    name: str
    custom: bool
    connect_portal_method: str
    type: MetricType
    configuration: _any_pb2.Any
    connected_metrics: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, connect_portal_uuid: _Optional[str] = ..., company_uuid: _Optional[str] = ..., key: _Optional[str] = ..., name: _Optional[str] = ..., custom: bool = ..., connect_portal_method: _Optional[str] = ..., type: _Optional[_Union[MetricType, str]] = ..., configuration: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., connected_metrics: _Optional[_Iterable[str]] = ...) -> None: ...

class MetricBulkCreateRequest(_message.Message):
    __slots__ = ["metrics", "connect_portal_uuid"]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    CONNECT_PORTAL_UUID_FIELD_NUMBER: _ClassVar[int]
    metrics: _containers.RepeatedCompositeFieldContainer[MetricCreateRequest]
    connect_portal_uuid: str
    def __init__(self, metrics: _Optional[_Iterable[_Union[MetricCreateRequest, _Mapping]]] = ..., connect_portal_uuid: _Optional[str] = ...) -> None: ...

class MetricUpdateRequest(_message.Message):
    __slots__ = ["metric_uuid", "name", "type", "configuration", "connected_metrics"]
    METRIC_UUID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_METRICS_FIELD_NUMBER: _ClassVar[int]
    metric_uuid: str
    name: str
    type: MetricType
    configuration: _any_pb2.Any
    connected_metrics: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, metric_uuid: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[_Union[MetricType, str]] = ..., configuration: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., connected_metrics: _Optional[_Iterable[str]] = ...) -> None: ...

class MetricDeleteRequest(_message.Message):
    __slots__ = ["metric_uuid"]
    METRIC_UUID_FIELD_NUMBER: _ClassVar[int]
    metric_uuid: str
    def __init__(self, metric_uuid: _Optional[str] = ...) -> None: ...

class MetricResponse(_message.Message):
    __slots__ = ["operation", "success", "uuid", "key", "name", "custom", "type", "connect_portal_uuid", "company_uuid", "connected_metrics", "connect_portal_method", "configuration", "created_at", "updated_at"]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONNECT_PORTAL_UUID_FIELD_NUMBER: _ClassVar[int]
    COMPANY_UUID_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_METRICS_FIELD_NUMBER: _ClassVar[int]
    CONNECT_PORTAL_METHOD_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    operation: OperationEnum
    success: bool
    uuid: str
    key: str
    name: str
    custom: bool
    type: MetricType
    connect_portal_uuid: str
    company_uuid: str
    connected_metrics: _containers.RepeatedScalarFieldContainer[str]
    connect_portal_method: str
    configuration: _any_pb2.Any
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, operation: _Optional[_Union[OperationEnum, str]] = ..., success: bool = ..., uuid: _Optional[str] = ..., key: _Optional[str] = ..., name: _Optional[str] = ..., custom: bool = ..., type: _Optional[_Union[MetricType, str]] = ..., connect_portal_uuid: _Optional[str] = ..., company_uuid: _Optional[str] = ..., connected_metrics: _Optional[_Iterable[str]] = ..., connect_portal_method: _Optional[str] = ..., configuration: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class MetricsResponse(_message.Message):
    __slots__ = ["operation", "success", "metrics"]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    operation: OperationEnum
    success: bool
    metrics: _containers.RepeatedCompositeFieldContainer[MetricResponse]
    def __init__(self, operation: _Optional[_Union[OperationEnum, str]] = ..., success: bool = ..., metrics: _Optional[_Iterable[_Union[MetricResponse, _Mapping]]] = ...) -> None: ...

class AvailableMetricsRequest(_message.Message):
    __slots__ = ["connect_portal_uuid"]
    CONNECT_PORTAL_UUID_FIELD_NUMBER: _ClassVar[int]
    connect_portal_uuid: str
    def __init__(self, connect_portal_uuid: _Optional[str] = ...) -> None: ...

class AvailableValues(_message.Message):
    __slots__ = ["metric_key", "values"]
    METRIC_KEY_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    metric_key: str
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, metric_key: _Optional[str] = ..., values: _Optional[_Iterable[str]] = ...) -> None: ...

class AvailableValuesResponse(_message.Message):
    __slots__ = ["available_values"]
    AVAILABLE_VALUES_FIELD_NUMBER: _ClassVar[int]
    available_values: _containers.RepeatedCompositeFieldContainer[AvailableValues]
    def __init__(self, available_values: _Optional[_Iterable[_Union[AvailableValues, _Mapping]]] = ...) -> None: ...

class AvailableValuesRequest(_message.Message):
    __slots__ = ["company_uuid", "metric_keys"]
    COMPANY_UUID_FIELD_NUMBER: _ClassVar[int]
    METRIC_KEYS_FIELD_NUMBER: _ClassVar[int]
    company_uuid: str
    metric_keys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, company_uuid: _Optional[str] = ..., metric_keys: _Optional[_Iterable[str]] = ...) -> None: ...
