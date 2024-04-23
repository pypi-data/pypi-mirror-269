import os
from typing import Iterable, Literal, Union, overload

import grpc
import grpc._grpcio_metadata

from vmxai.auth.provider import VMXClientAuthProvider
from vmxai.protos.completion.completion_pb2 import CompletionRequest, CompletionResponse
from vmxai.protos.completion.completion_pb2_grpc import CompletionServiceStub


class VMXClient:
    def __init__(self, workspace_id: str, environment_id: str, domain: str, auth: VMXClientAuthProvider):
        self.workspace_id = workspace_id
        self.environment_id = environment_id
        self.domain = domain
        self.auth = auth

        channel = grpc.secure_channel(f"grpc.{self.domain}", grpc.ssl_channel_credentials())

        self.completion_client = CompletionServiceStub(channel)

    @overload
    def completion(self, request: CompletionRequest) -> Iterable[CompletionResponse]: ...

    @overload
    def completion(self, request: CompletionRequest, stream: Literal[True]) -> Iterable[CompletionResponse]: ...

    @overload
    def completion(self, request: CompletionRequest, stream: Literal[False]) -> CompletionResponse: ...

    def completion(
        self, request: CompletionRequest, stream: bool = True
    ) -> Union[CompletionResponse, Iterable[CompletionResponse]]:
        metadata: list[tuple[str, str]] = []
        if "_X_AMZN_TRACE_ID" in os.environ:
            metadata.append(("x-amzn-trace-id", os.environ["_X_AMZN_TRACE_ID"]))

        self.auth.inject_credentials(self, metadata)
        request.stream = stream

        if stream:
            return self.completion_client.create(request, metadata=tuple(metadata))
        else:
            for response in self.completion_client.create(request, metadata=metadata):
                return response
