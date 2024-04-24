from aiovemmio import pubsub_pb2 as _pubsub_pb2
from aiovemmio import reports_pb2 as _reports_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WebsocketMessage(_message.Message):
    __slots__ = ["frame_id", "gateway_report", "reply", "request"]
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    GATEWAY_REPORT_FIELD_NUMBER: _ClassVar[int]
    REPLY_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    frame_id: int
    gateway_report: _reports_pb2.GatewayReport
    reply: _pubsub_pb2.CommandReply
    request: _pubsub_pb2.CommandRequest
    def __init__(self, frame_id: _Optional[int] = ..., request: _Optional[_Union[_pubsub_pb2.CommandRequest, _Mapping]] = ..., reply: _Optional[_Union[_pubsub_pb2.CommandReply, _Mapping]] = ..., gateway_report: _Optional[_Union[_reports_pb2.GatewayReport, _Mapping]] = ...) -> None: ...
