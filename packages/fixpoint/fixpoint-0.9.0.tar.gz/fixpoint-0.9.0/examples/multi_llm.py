"""Example of multi-LLM routing"""

from dataclasses import dataclass
import os

from fixpoint import openapi_client, FixpointClient


@dataclass
class ApiKeys:
    """Various API keys"""

    fixpoint: str
    anthropic: str
    openai: str


def main(apikeys: ApiKeys) -> None:
    """Example of multi-LLM routing

    When you make a MultiLLMChatCompletion request, it will make multiple LLM
    inference requests at once. Your client code will receive the chat
    completion back for the first model specified, while all subsequent model
    inference requests occur in the background (aka they do not block your first
    request from returning).

    All inference requests are logged to Fixpoint, and you can find sibling
    requests because all siblings will have the same `parent_span_id` set to
    equal the `span_id` that you passed in on the request. Or if you don't have
    multiple LLM inference requests in the same trace, you can find all sibling
    chat completions by filtering to the `trace_id`.
    """
    client = FixpointClient(
        fixpoint_api_key=apikeys.fixpoint,
        openai_api_key=apikeys.openai,
    )

    print("\nWaiting for inference...\n\n")

    multi_completion = client.fixpoint.api.fixpoint_create_multi_llm_chat_completion(
        openapi_client.V1CreateMultiLLMChatCompletionRequest(
            mode=openapi_client.V1Mode.MODE_TEST,
            models=[
                # This is the model response the Fixpoint API will return to the client
                openapi_client.V1CreateMultiLLMChatCompletionRequestModel(
                    name="anthropic/claude-3-sonnet-20240229",
                    temperature=1.0,
                    api_key=apikeys.anthropic,
                    max_tokens=1024,
                ),
                # These model chat completion requests will be made in the background
                openapi_client.V1CreateMultiLLMChatCompletionRequestModel(
                    name="openai/gpt-3.5-turbo-1106",
                    temperature=1.8,
                    api_key=apikeys.openai,
                ),
                openapi_client.V1CreateMultiLLMChatCompletionRequestModel(
                    name="openai/gpt-3.5-turbo-1106",
                    temperature=0.9,
                    api_key=apikeys.openai,
                ),
            ],
            messages=[
                openapi_client.V1InputMessage(
                    role="system",
                    content="You are an old curmudgeonly AI. You are helpful, but you don't like being helpful. You are concise.",  # pylint: disable=line-too-long
                ),
                openapi_client.V1InputMessage(
                    role="user", content="How does ChatGPT work?"
                ),
            ],
            # Specify tracing info so that we can correlate these multi-LLM
            # requests and see what the different base models generated.
            tracing=openapi_client.V1Tracing(
                # All children inference requests (one for each model above)
                # will share this session ID.
                session_id="27eea3a1-e16e-4643-aa0c-4b0cdb4e826b",
                # All children inference requests share this trace ID.
                trace_id="trace_id",
                # All children inference requests have `parent_span_id` set to this.
                span_id="46425bf0-6e48-4018-9e34-7539627a09ea",
                parent_span_id="d6156682-70bd-430b-9701-50c20fc4bf39",
            ),
            user_id="dylan",
            # You can also attach log attributes to the LLM requests. This can
            # be useful if you are doing an experiment to try out different LLM
            # models.
            log_attributes=[
                openapi_client.V1LogAttribute(
                    key="experiment", value="multi-llm-example"
                )
            ],
        )
    )

    completion_id = multi_completion.id
    external_id = multi_completion.primary_external_id
    print(
        f"Made MultiLLMCompletion with ID: {completion_id}, External ID: {external_id}\n"
    )
    choice = multi_completion.completion.choices[0]
    role = choice.message.role
    content = choice.message.content
    print(f"{role}: {content}")


if __name__ == "__main__":
    main(
        ApiKeys(
            fixpoint=os.environ["FIXPOINT_API_KEY"],
            anthropic=os.environ["ANTHROPIC_API_KEY"],
            openai=os.environ["OPENAI_API_KEY"],
        )
    )
