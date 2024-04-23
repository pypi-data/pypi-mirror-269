# VM-X SDK for Python

## Description

VM-X AI SDK client for Python

## Installation

```bash
pip install vm-x-ai-sdk
```

```bash
poetry add vm-x-ai-sdk
```

## Usage

```python
from vmxai import CompletionRequest, OpenAIRequest, RequestMessage, VMXClient, VMXClientOAuth

client = VMXClient(
    workspace_id="ws-abc123",
    environment_id="env-abv123",
    domain="env-abc123.clnt.vm-x.ai",
    auth=VMXClientOAuth(
        client_id="clientId", client_secret="clientSecret"
    ),
)

result = client.completion(
    CompletionRequest(
        provider="openai",
        resource="my-resource",
        workload="my-workload",
        messages=[RequestMessage(role="user", content="hey")],
        functions=[],
        openai=OpenAIRequest(model="gpt-3.5-turbo"),
    ),
    stream=True,
)

for message in result:
    print(message.message)

```

## [Change Log](./CHANGELOG.md)
