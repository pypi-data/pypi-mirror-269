from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RequestFunctions(_message.Message):
    __slots__ = ("description", "name", "parameters")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    description: str
    name: str
    parameters: _struct_pb2.Struct
    def __init__(self, description: _Optional[str] = ..., name: _Optional[str] = ..., parameters: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class RequestFunctionCall(_message.Message):
    __slots__ = ("auto", "none", "function")
    AUTO_FIELD_NUMBER: _ClassVar[int]
    NONE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    auto: bool
    none: bool
    function: RequestFunctionCallName
    def __init__(self, auto: bool = ..., none: bool = ..., function: _Optional[_Union[RequestFunctionCallName, _Mapping]] = ...) -> None: ...

class RequestFunctionCallName(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class RequestMessage(_message.Message):
    __slots__ = ("name", "role", "content", "function_call")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_CALL_FIELD_NUMBER: _ClassVar[int]
    name: str
    role: str
    content: str
    function_call: RequestMessageFunctionCall
    def __init__(self, name: _Optional[str] = ..., role: _Optional[str] = ..., content: _Optional[str] = ..., function_call: _Optional[_Union[RequestMessageFunctionCall, _Mapping]] = ...) -> None: ...

class RequestMessageFunctionCall(_message.Message):
    __slots__ = ("name", "arguments")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    name: str
    arguments: str
    def __init__(self, name: _Optional[str] = ..., arguments: _Optional[str] = ...) -> None: ...

class OpenAIRequest(_message.Message):
    __slots__ = ("model", "frequency_penalty", "max_tokens", "presence_penalty", "temperature")
    MODEL_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_PENALTY_FIELD_NUMBER: _ClassVar[int]
    MAX_TOKENS_FIELD_NUMBER: _ClassVar[int]
    PRESENCE_PENALTY_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    model: str
    frequency_penalty: float
    max_tokens: int
    presence_penalty: float
    temperature: float
    def __init__(self, model: _Optional[str] = ..., frequency_penalty: _Optional[float] = ..., max_tokens: _Optional[int] = ..., presence_penalty: _Optional[float] = ..., temperature: _Optional[float] = ...) -> None: ...

class GeminiRequest(_message.Message):
    __slots__ = ("model", "max_output_tokens", "temperature")
    MODEL_FIELD_NUMBER: _ClassVar[int]
    MAX_OUTPUT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    model: str
    max_output_tokens: int
    temperature: float
    def __init__(self, model: _Optional[str] = ..., max_output_tokens: _Optional[int] = ..., temperature: _Optional[float] = ...) -> None: ...

class CompletionRequest(_message.Message):
    __slots__ = ("resource", "workload", "provider", "stream", "messages", "functions", "function_call", "openai", "gemini")
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    WORKLOAD_FIELD_NUMBER: _ClassVar[int]
    PROVIDER_FIELD_NUMBER: _ClassVar[int]
    STREAM_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    FUNCTIONS_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_CALL_FIELD_NUMBER: _ClassVar[int]
    OPENAI_FIELD_NUMBER: _ClassVar[int]
    GEMINI_FIELD_NUMBER: _ClassVar[int]
    resource: str
    workload: str
    provider: str
    stream: bool
    messages: _containers.RepeatedCompositeFieldContainer[RequestMessage]
    functions: _containers.RepeatedCompositeFieldContainer[RequestFunctions]
    function_call: RequestFunctionCall
    openai: OpenAIRequest
    gemini: GeminiRequest
    def __init__(self, resource: _Optional[str] = ..., workload: _Optional[str] = ..., provider: _Optional[str] = ..., stream: bool = ..., messages: _Optional[_Iterable[_Union[RequestMessage, _Mapping]]] = ..., functions: _Optional[_Iterable[_Union[RequestFunctions, _Mapping]]] = ..., function_call: _Optional[_Union[RequestFunctionCall, _Mapping]] = ..., openai: _Optional[_Union[OpenAIRequest, _Mapping]] = ..., gemini: _Optional[_Union[GeminiRequest, _Mapping]] = ...) -> None: ...

class CompletionResponse(_message.Message):
    __slots__ = ("id", "message", "role", "function_call", "usage", "response_timestamp")
    ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_CALL_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    id: str
    message: str
    role: str
    function_call: RequestMessageFunctionCall
    usage: CompletionUsage
    response_timestamp: int
    def __init__(self, id: _Optional[str] = ..., message: _Optional[str] = ..., role: _Optional[str] = ..., function_call: _Optional[_Union[RequestMessageFunctionCall, _Mapping]] = ..., usage: _Optional[_Union[CompletionUsage, _Mapping]] = ..., response_timestamp: _Optional[int] = ...) -> None: ...

class CompletionUsage(_message.Message):
    __slots__ = ("prompt", "completion", "total")
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    prompt: int
    completion: int
    total: int
    def __init__(self, prompt: _Optional[int] = ..., completion: _Optional[int] = ..., total: _Optional[int] = ...) -> None: ...
