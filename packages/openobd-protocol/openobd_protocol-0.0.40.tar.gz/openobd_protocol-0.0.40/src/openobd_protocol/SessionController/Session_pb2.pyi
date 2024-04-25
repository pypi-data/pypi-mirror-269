from openobd_protocol import Status_pb2 as _Status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StartSession(_message.Message):
    __slots__ = ("connection_uuid",)
    CONNECTION_UUID_FIELD_NUMBER: _ClassVar[int]
    connection_uuid: str
    def __init__(self, connection_uuid: _Optional[str] = ...) -> None: ...

class SessionInfo(_message.Message):
    __slots__ = ("id", "session_status", "created_at", "session_endpoint", "authentication_token")
    ID_FIELD_NUMBER: _ClassVar[int]
    SESSION_STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    SESSION_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    id: str
    session_status: str
    created_at: str
    session_endpoint: str
    authentication_token: str
    def __init__(self, id: _Optional[str] = ..., session_status: _Optional[str] = ..., created_at: _Optional[str] = ..., session_endpoint: _Optional[str] = ..., authentication_token: _Optional[str] = ...) -> None: ...

class Authenticate(_message.Message):
    __slots__ = ("client_id", "client_credentials", "api_key")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_credentials: str
    api_key: str
    def __init__(self, client_id: _Optional[str] = ..., client_credentials: _Optional[str] = ..., api_key: _Optional[str] = ...) -> None: ...

class SessionToken(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class SessionInfoList(_message.Message):
    __slots__ = ("sessions",)
    SESSIONS_FIELD_NUMBER: _ClassVar[int]
    sessions: _containers.RepeatedCompositeFieldContainer[SessionInfo]
    def __init__(self, sessions: _Optional[_Iterable[_Union[SessionInfo, _Mapping]]] = ...) -> None: ...

class SessionId(_message.Message):
    __slots__ = ("session_id",)
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    session_id: str
    def __init__(self, session_id: _Optional[str] = ...) -> None: ...
