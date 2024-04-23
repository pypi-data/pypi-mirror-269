from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class startSession(_message.Message):
    __slots__ = ("client_id", "client_credentials", "api_key", "connection_uuid")
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_UUID_FIELD_NUMBER: _ClassVar[int]
    client_id: str
    client_credentials: str
    api_key: str
    connection_uuid: str
    def __init__(self, client_id: _Optional[str] = ..., client_credentials: _Optional[str] = ..., api_key: _Optional[str] = ..., connection_uuid: _Optional[str] = ...) -> None: ...

class sessionInfo(_message.Message):
    __slots__ = ("id", "status", "created_at", "session_endpoint", "authentication_token")
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    SESSION_ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: str
    created_at: str
    session_endpoint: str
    authentication_token: str
    def __init__(self, id: _Optional[str] = ..., status: _Optional[str] = ..., created_at: _Optional[str] = ..., session_endpoint: _Optional[str] = ..., authentication_token: _Optional[str] = ...) -> None: ...
