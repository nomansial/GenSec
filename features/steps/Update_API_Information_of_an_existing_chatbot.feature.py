import requests
import logging
from behave import given, when, then
from assertpy import assert_that
from utilities.configurations import getConfig

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@given(u'User sends PUT request to update chatbot API details for chatbot ID with environment ID and endpoint "{chatbot_url}"')
def step_impl(context, chatbot_url):
    """Create chatbot, wait until status is AVAILABLE, then send PUT request to update it"""
    import time

    config = getConfig()
    base_url = config['API']['BaseURL']
    api_key = config['API']['APIKey']

    # POST request to create chatbot
    context.url = f"{base_url}/chatbots"
    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    chatbot_name = "QA Automation"
    chatbot_description = "System testing please ignore"
    env_id = "f0b53f20-5ebe-4132-cbea-68725ef2c5c8"

    payload = {
        "env_id": env_id,
        "chatbot_name": chatbot_name,
        "api_endpoint": "Jr.lzPApNRNNQR:n1Xy6WyKDPWvA@1eR5t#302OYb%lnp4ehZGwDWPoaeEDF7Nnt_hDPuK9Po2crHTiqXd-zVT9rHwiVXBEg@QvomKrjMHbJIJ8-mIswCmUY0+eYO4ZlqAg4YDUcbF@5zMaS.fozhq",
        "api_secret": "wVyB2",
        "chatbot_url": "www.t@TiGfZIdBeat:+B5XsEP4ZPRB0ZB1UI-dcArK64u@6hhfa#D8cZ+LyR:Nd0Z-glOD9q7qDSWPmJdVEx.aDTK3%#9itUKB4v7xikDUBbG~pA=qD9rVjfz6hAxgsOjZBWIkp%jyLpZj#caaQrBL",
        "chatbot_description": chatbot_description
    }

    context.response = requests.post(context.url, json=payload, headers=context.headers)
    logger.info(f"Create Chatbot API Response: {context.response.text}")
    print(f"Create Chatbot API Response: {context.response.text}")

    chatbot_id = context.response.json().get("chatbot_id")
    context.chatbot_id = chatbot_id
    assert chatbot_id is not None, "chatbot_id not found in response"

    # Poll until status becomes AVAILABLE
    status_url = f"{base_url}/chatbots/{chatbot_id}"
    max_retries = 100
    wait_seconds = 10

    for attempt in range(max_retries):
        status_response = requests.get(status_url, headers={'x-api-key': api_key})
        status = status_response.json().get("status")
        logger.info(f"Attempt {attempt + 1}: Chatbot status = {status}")
        print(f"Attempt {attempt + 1}: Chatbot status = {status}")

        if status == "AVAILABLE":
            # Send PUT request to update  details
            context.url = f"{config['API']['BaseURL']}/chatbots/{chatbot_id}/api"

            payload = {
                "chatbot_id": chatbot_id,
                "env_id": env_id,
                "chatbot_url": chatbot_url,
                "api_endpoint": "/stream_messages",
                "api_specifications": "{\"openapi\":\"3.1.0\",\"info\":{\"title\":\"test-chatbot\",\"description\":\"API for interacting with the Agent test-chatbot\",\"version\":\"0.1.0\"},\"paths\":{\"\/\":{\"get\":{\"summary\":\"Redirect Root To Docs\",\"description\":\"Redirect the root URL to the API documentation.\",\"operationId\":\"redirect_root_to_docs__get\",\"responses\":{\"307\":{\"description\":\"Successful Response\"}}}},\"\/feedback\":{\"post\":{\"summary\":\"Collect Feedback\",\"description\":\"Collect and log feedback.\\n\\nArgs:\\n    feedback: The feedback data to log\\n\\nReturns:\\n    Success message\",\"operationId\":\"collect_feedback_feedback_post\",\"requestBody\":{\"content\":{\"application\/json\":{\"schema\":{\"$ref\":\"#\/components\/schemas\/Feedback\"}}},\"required\":true},\"responses\":{\"200\":{\"description\":\"Successful Response\",\"content\":{\"application\/json\":{\"schema\":{\"additionalProperties\":{\"type\":\"string\"},\"type\":\"object\",\"title\":\"Response Collect Feedback Feedback Post\"}}}},\"422\":{\"description\":\"Validation Error\",\"content\":{\"application\/json\":{\"schema\":{\"$ref\":\"#\/components\/schemas\/HTTPValidationError\"}}}}}}},\"\/stream_messages\":{\"post\":{\"summary\":\"Stream Chat Events\",\"description\":\"Stream chat events in response to an input request.\\n\\nArgs:\\n    request: The chat request containing input and config\\n\\nReturns:\\n    Streaming response of chat events\",\"operationId\":\"stream_chat_events_stream_messages_post\",\"requestBody\":{\"content\":{\"application\/json\":{\"schema\":{\"$ref\":\"#\/components\/schemas\/Request\"}}},\"required\":true},\"responses\":{\"200\":{\"description\":\"Successful Response\",\"content\":{\"application\/json\":{\"schema\":{}}}},\"422\":{\"description\":\"Validation Error\",\"content\":{\"application\/json\":{\"schema\":{\"$ref\":\"#\/components\/schemas\/HTTPValidationError\"}}}}}}}},\"components\":{\"schemas\":{\"AIMessage\":{\"properties\":{\"content\":{\"anyOf\":[{\"type\":\"string\"},{\"items\":{\"anyOf\":[{\"type\":\"string\"},{\"additionalProperties\":true,\"type\":\"object\"}]},\"type\":\"array\"}],\"title\":\"Content\"},\"additional_kwargs\":{\"additionalProperties\":true,\"type\":\"object\",\"title\":\"Additional Kwargs\"},\"response_metadata\":{\"additionalProperties\":true,\"type\":\"object\",\"title\":\"Response Metadata\"},\"type\":{\"type\":\"string\",\"const\":\"ai\",\"title\":\"Type\",\"default\":\"ai\"},\"name\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Name\"},\"id\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Id\"},\"example\":{\"type\":\"boolean\",\"title\":\"Example\",\"default\":false},\"tool_calls\":{\"items\":{\"$ref\":\"#\/components\/schemas\/ToolCall\"},\"type\":\"array\",\"title\":\"Tool Calls\",\"default\":[]},\"invalid_tool_calls\":{\"items\":{\"$ref\":\"#\/components\/schemas\/InvalidToolCall\"},\"type\":\"array\",\"title\":\"Invalid Tool Calls\",\"default\":[]},\"usage_metadata\":{\"anyOf\":[{\"$ref\":\"#\/components\/schemas\/UsageMetadata\"},{\"type\":\"null\"}]}},\"additionalProperties\":true,\"type\":\"object\",\"required\":[\"content\"],\"title\":\"AIMessage\",\"description\":\"Message from an AI.\\n\\nAIMessage is returned from a chat model as a response to a prompt.\\n\\nThis message represents the output of the model and consists of both\\nthe raw output as returned by the model together standardized fields\\n(e.g., tool calls, usage metadata) added by the LangChain framework.\"},\"Feedback\":{\"properties\":{\"score\":{\"anyOf\":[{\"type\":\"integer\"},{\"type\":\"number\"}],\"title\":\"Score\"},\"text\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Text\",\"default\":\"\"},\"run_id\":{\"type\":\"string\",\"title\":\"Run Id\"},\"log_type\":{\"type\":\"string\",\"const\":\"feedback\",\"title\":\"Log Type\",\"default\":\"feedback\"},\"service_name\":{\"type\":\"string\",\"const\":\"test-chatbot\",\"title\":\"Service Name\",\"default\":\"test-chatbot\"}},\"type\":\"object\",\"required\":[\"score\",\"run_id\"],\"title\":\"Feedback\",\"description\":\"Represents feedback for a conversation.\"},\"HTTPValidationError\":{\"properties\":{\"detail\":{\"items\":{\"$ref\":\"#\/components\/schemas\/ValidationError\"},\"type\":\"array\",\"title\":\"Detail\"}},\"type\":\"object\",\"title\":\"HTTPValidationError\"},\"HumanMessage\":{\"properties\":{\"content\":{\"anyOf\":[{\"type\":\"string\"},{\"items\":{\"anyOf\":[{\"type\":\"string\"},{\"additionalProperties\":true,\"type\":\"object\"}]},\"type\":\"array\"}],\"title\":\"Content\"},\"additional_kwargs\":{\"additionalProperties\":true,\"type\":\"object\",\"title\":\"Additional Kwargs\"},\"response_metadata\":{\"additionalProperties\":true,\"type\":\"object\",\"title\":\"Response Metadata\"},\"type\":{\"type\":\"string\",\"const\":\"human\",\"title\":\"Type\",\"default\":\"human\"},\"name\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Name\"},\"id\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Id\"},\"example\":{\"type\":\"boolean\",\"title\":\"Example\",\"default\":false}},\"additionalProperties\":true,\"type\":\"object\",\"required\":[\"content\"],\"title\":\"HumanMessage\",\"description\":\"Message from a human.\\n\\nHumanMessages are messages that are passed in from a human to the model.\\n\\nExample:\\n\\n    .. code-block:: python\\n\\n        from langchain_core.messages import HumanMessage, SystemMessage\\n\\n        messages = [\\n            SystemMessage(\\n                content=\\\"You are a helpful assistant! Your name is Bob.\\\"\\n            ),\\n            HumanMessage(\\n                content=\\\"What is your name?\\\"\\n            )\\n        ]\\n\\n        # Instantiate a chat model and invoke it with the messages\\n        model = ...\\n        print(model.invoke(messages))\"},\"InputChat\":{\"properties\":{\"messages\":{\"items\":{\"oneOf\":[{\"$ref\":\"#\/components\/schemas\/HumanMessage\"},{\"$ref\":\"#\/components\/schemas\/AIMessage\"},{\"$ref\":\"#\/components\/schemas\/ToolMessage\"}],\"discriminator\":{\"propertyName\":\"type\",\"mapping\":{\"ai\":\"#\/components\/schemas\/AIMessage\",\"human\":\"#\/components\/schemas\/HumanMessage\",\"tool\":\"#\/components\/schemas\/ToolMessage\"}}},\"type\":\"array\",\"title\":\"Messages\",\"description\":\"The chat messages representing the current conversation.\"}},\"type\":\"object\",\"required\":[\"messages\"],\"title\":\"InputChat\",\"description\":\"Represents the input for a chat session.\"},\"InputTokenDetails\":{\"properties\":{\"audio\":{\"type\":\"integer\",\"title\":\"Audio\"},\"cache_creation\":{\"type\":\"integer\",\"title\":\"Cache Creation\"},\"cache_read\":{\"type\":\"integer\",\"title\":\"Cache Read\"}},\"type\":\"object\",\"title\":\"InputTokenDetails\",\"description\":\"Breakdown of input token counts.\\n\\nDoes *not* need to sum to full input token count. Does *not* need to have all keys.\\n\\nExample:\\n\\n    .. code-block:: python\\n\\n        {\\n            \\\"audio\\\": 10,\\n            \\\"cache_creation\\\": 200,\\n            \\\"cache_read\\\": 100,\\n        }\\n\\n.. versionadded:: 0.3.9\\n\\nMay also hold extra provider-specific keys.\"},\"InvalidToolCall\":{\"properties\":{\"name\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Name\"},\"args\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Args\"},\"id\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Id\"},\"error\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Error\"},\"type\":{\"type\":\"string\",\"const\":\"invalid_tool_call\",\"title\":\"Type\"}},\"type\":\"object\",\"required\":[\"name\",\"args\",\"id\",\"error\"],\"title\":\"InvalidToolCall\",\"description\":\"Allowance for errors made by LLM.\\n\\nHere we add an `error` key to surface errors made during generation\\n(e.g., invalid JSON arguments.)\"},\"OutputTokenDetails\":{\"properties\":{\"audio\":{\"type\":\"integer\",\"title\":\"Audio\"},\"reasoning\":{\"type\":\"integer\",\"title\":\"Reasoning\"}},\"type\":\"object\",\"title\":\"OutputTokenDetails\",\"description\":\"Breakdown of output token counts.\\n\\nDoes *not* need to sum to full output token count. Does *not* need to have all keys.\\n\\nExample:\\n\\n    .. code-block:: python\\n\\n        {\\n            \\\"audio\\\": 10,\\n            \\\"reasoning\\\": 200,\\n        }\\n\\n.. versionadded:: 0.3.9\"},\"Request\":{\"properties\":{\"input\":{\"$ref\":\"#\/components\/schemas\/InputChat\"},\"config\":{\"anyOf\":[{\"$ref\":\"#\/components\/schemas\/RunnableConfig\"},{\"type\":\"null\"}]}},\"type\":\"object\",\"required\":[\"input\"],\"title\":\"Request\",\"description\":\"Represents the input for a chat request with optional configuration.\\n\\nAttributes:\\n    input: The chat input containing messages and other chat-related data\\n    config: Optional configuration for the runnable, including tags, callbacks, etc.\"},\"RunnableConfig\":{\"properties\":{\"tags\":{\"items\":{\"type\":\"string\"},\"type\":\"array\",\"title\":\"Tags\"},\"metadata\":{\"additionalProperties\":true,\"type\":\"object\",\"title\":\"Metadata\"},\"callbacks\":{\"anyOf\":[{\"items\":{},\"type\":\"array\"},{},{\"type\":\"null\"}],\"title\":\"Callbacks\"},\"run_name\":{\"type\":\"string\",\"title\":\"Run Name\"},\"max_concurrency\":{\"anyOf\":[{\"type\":\"integer\"},{\"type\":\"null\"}],\"title\":\"Max Concurrency\"},\"recursion_limit\":{\"type\":\"integer\",\"title\":\"Recursion Limit\"},\"configurable\":{\"additionalProperties\":true,\"type\":\"object\",\"title\":\"Configurable\"},\"run_id\":{\"anyOf\":[{\"type\":\"string\",\"format\":\"uuid\"},{\"type\":\"null\"}],\"title\":\"Run Id\"}},\"type\":\"object\",\"title\":\"RunnableConfig\",\"description\":\"Configuration for a Runnable.\"},\"ToolCall\":{\"properties\":{\"name\":{\"type\":\"string\",\"title\":\"Name\"},\"args\":{\"additionalProperties\":true,\"type\":\"object\",\"title\":\"Args\"},\"id\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Id\"},\"type\":{\"type\":\"string\",\"const\":\"tool_call\",\"title\":\"Type\"}},\"type\":\"object\",\"required\":[\"name\",\"args\",\"id\"],\"title\":\"ToolCall\",\"description\":\"Represents a request to call a tool.\\n\\nExample:\\n\\n    .. code-block:: python\\n\\n        {\\n            \\\"name\\\": \\\"foo\\\",\\n            \\\"args\\\": {\\\"a\\\": 1},\\n            \\\"id\\\": \\\"123\\\"\\n        }\\n\\n    This represents a request to call the tool named \\\"foo\\\" with arguments {\\\"a\\\": 1}\\n    and an identifier of \\\"123\\\".\"},\"ToolMessage\":{\"properties\":{\"content\":{\"anyOf\":[{\"type\":\"string\"},{\"items\":{\"anyOf\":[{\"type\":\"string\"},{\"additionalProperties\":true,\"type\":\"object\"}]},\"type\":\"array\"}],\"title\":\"Content\"},\"additional_kwargs\":{\"additionalProperties\":true,\"type\":\"object\",\"title\":\"Additional Kwargs\"},\"response_metadata\":{\"additionalProperties\":true,\"type\":\"object\",\"title\":\"Response Metadata\"},\"type\":{\"type\":\"string\",\"const\":\"tool\",\"title\":\"Type\",\"default\":\"tool\"},\"name\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Name\"},\"id\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Id\"},\"tool_call_id\":{\"type\":\"string\",\"title\":\"Tool Call Id\"},\"artifact\":{\"title\":\"Artifact\"},\"status\":{\"type\":\"string\",\"enum\":[\"success\",\"error\"],\"title\":\"Status\",\"default\":\"success\"}},\"additionalProperties\":true,\"type\":\"object\",\"required\":[\"content\",\"tool_call_id\"],\"title\":\"ToolMessage\",\"description\":\"Message for passing the result of executing a tool back to a model.\\n\\nToolMessages contain the result of a tool invocation. Typically, the result\\nis encoded inside the `content` field.\\n\\nExample: A ToolMessage representing a result of 42 from a tool call with id\\n\\n    .. code-block:: python\\n\\n        from langchain_core.messages import ToolMessage\\n\\n        ToolMessage(content='42', tool_call_id='call_Jja7J89XsjrOLA5r!MEOW!SL')\\n\\n\\nExample: A ToolMessage where only part of the tool output is sent to the model\\n    and the full output is passed in to artifact.\\n\\n    .. versionadded:: 0.2.17\\n\\n    .. code-block:: python\\n\\n        from langchain_core.messages import ToolMessage\\n\\n        tool_output = {\\n            \\\"stdout\\\": \\\"From the graph we can see that the correlation between x and y is ...\\\",\\n            \\\"stderr\\\": None,\\n            \\\"artifacts\\\": {\\\"type\\\": \\\"image\\\", \\\"base64_data\\\": \\\"\/9j\/4gIcSU...\\\"},\\n        }\\n\\n        ToolMessage(\\n            content=tool_output[\\\"stdout\\\"],\\n            artifact=tool_output,\\n            tool_call_id='call_Jja7J89XsjrOLA5r!MEOW!SL',\\n        )\\n\\nThe tool_call_id field is used to associate the tool call request with the\\ntool call response. This is useful in situations where a chat model is able\\nto request multiple tool calls in parallel.\"},\"UsageMetadata\":{\"properties\":{\"input_tokens\":{\"type\":\"integer\",\"title\":\"Input Tokens\"},\"output_tokens\":{\"type\":\"integer\",\"title\":\"Output Tokens\"},\"total_tokens\":{\"type\":\"integer\",\"title\":\"Total Tokens\"},\"input_token_details\":{\"$ref\":\"#\/components\/schemas\/InputTokenDetails\"},\"output_token_details\":{\"$ref\":\"#\/components\/schemas\/OutputTokenDetails\"}},\"type\":\"object\",\"required\":[\"input_tokens\",\"output_tokens\",\"total_tokens\"],\"title\":\"UsageMetadata\",\"description\":\"Usage metadata for a message, such as token counts.\\n\\nThis is a standard representation of token usage that is consistent across models.\\n\\nExample:\\n\\n    .. code-block:: python\\n\\n        {\\n            \\\"input_tokens\\\": 350,\\n            \\\"output_tokens\\\": 240,\\n            \\\"total_tokens\\\": 590,\\n            \\\"input_token_details\\\": {\\n                \\\"audio\\\": 10,\\n                \\\"cache_creation\\\": 200,\\n                \\\"cache_read\\\": 100,\\n            },\\n            \\\"output_token_details\\\": {\\n                \\\"audio\\\": 10,\\n                \\\"reasoning\\\": 200,\\n            }\\n        }\\n\\n.. versionchanged:: 0.3.9\\n\\n    Added ``input_token_details`` and ``output_token_details``.\"},\"ValidationError\":{\"properties\":{\"loc\":{\"items\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"integer\"}]},\"type\":\"array\",\"title\":\"Location\"},\"msg\":{\"type\":\"string\",\"title\":\"Message\"},\"type\":{\"type\":\"string\",\"title\":\"Error Type\"}},\"type\":\"object\",\"required\":[\"loc\",\"msg\",\"type\"],\"title\":\"ValidationError\"}}}}\"\r\n  \"api_endpoint\": \"\/stream_messages",
                "chatbot_name": "AutomationChatBoat"
            }

            api_key = config['API']['APIKey']
            context.headers = {
                'Content-Type': 'application/json',
                'x-api-key': api_key
            }

            context.response2 = requests.put(context.url, headers=context.headers, json=payload)
            logger.info(f"Update API Information of an existing Response: {context.response.text}")
            print(f"Update API Information of an existing Response: {context.response.text}")
            return

        time.sleep(wait_seconds)

    assert False, f"Chatbot status did not become AVAILABLE after {max_retries} attempts"

@given(u'User sends PUT request to update chatbot API details for chatbot ID "{chatbot_id}" with environment ID "{env_id}" and endpoint "{chatbot_url}"')
def step_impl(context, chatbot_id, env_id, chatbot_url):
    config = getConfig()
    base_url = config['API']['BaseURL']
    api_key = config['API']['APIKey']

    context.chatbot_id = chatbot_id  # Store for later validation
    context.url = f"{base_url}/chatbots/{chatbot_id}/api"
    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    payload = {
        "chatbot_id": chatbot_id,
        "env_id": env_id,
        "chatbot_url": chatbot_url,
        "api_endpoint": "/stream_messages",
        "api_specifications": "{\"openapi\":\"3.1.0\",\"info\":{\"title\":\"test-chatbot\",\"description\":\"API for interacting with the Agent test-chatbot\",\"version\":\"0.1.0\"},\"paths\":{\"\/\":{\"get\":{\"summary\":\"Redirect Root To Docs\",\"description\":\"Redirect the root URL to the API documentation.\",\"operationId\":\"redirect_root_to_docs__get\",\"responses\":{\"307\":{\"description\":\"Successful Response\"}}}},\"\/feedback\":{\"post\":{\"summary\":\"Collect Feedback\",\"description\":\"Collect and log feedback.\\n\\nArgs:\\n    feedback: The feedback data to log\\n\\nReturns:\\n    Success message\",\"operationId\":\"collect_feedback_feedback_post\",\"requestBody\":{\"content\":{\"application\/json\":{\"schema\":{\"$ref\":\"#\/components\/schemas\/Feedback\"}}},\"required\":true},\"responses\":{\"200\":{\"description\":\"Successful Response\",\"content\":{\"application\/json\":{\"schema\":{\"additionalProperties\":{\"type\":\"string\"},\"type\":\"object\",\"title\":\"Response Collect Feedback Feedback Post\"}}}},\"422\":{\"description\":\"Validation Error\",\"content\":{\"application\/json\":{\"schema\":{\"$ref\":\"#\/components\/schemas\/HTTPValidationError\"}}}}}}},\"\/stream_messages\":{\"post\":{\"summary\":\"Stream Chat Events\",\"description\":\"Stream chat events in response to an input request.\\n\\nArgs:\\n    request: The chat request containing input and config\\n\\nReturns:\\n    Streaming response of chat events\",\"operationId\":\"stream_chat_events_stream_messages_post\",\"requestBody\":{\"content\":{\"application\/json\":{\"schema\":{\"$ref\":\"#\/components\/schemas\/Request\"}}},\"required\":true},\"responses\":{\"200\":{\"description\":\"Successful Response\",\"content\":{\"application\/json\":{\"schema\":{}}}},\"422\":{\"description\":\"Validation Error\",\"content\":{\"application\/json\":{\"schema\":{\"$ref\":\"#\/components\/schemas\/HTTPValidationError\"}}}}}}}},\"components\":{\"schemas\":{\"AIMessage\":{\"properties\":{\"content\":{\"anyOf\":[{\"type\":\"string\"},{\"items\":{\"anyOf\":[{\"type\":\"string\"},{\"additionalProperties\":true,\"type\":\"object\"}]},\"type\":\"array\"}],\"title\":\"Content\"},\"additional_kwargs\":{\"additionalProperties\":true,\"type\":\"object\",\"title\":\"Additional Kwargs\"},\"response_metadata\":{\"additionalProperties\":true,\"type\":\"object\",\"title\":\"Response Metadata\"},\"type\":{\"type\":\"string\",\"const\":\"ai\",\"title\":\"Type\",\"default\":\"ai\"},\"name\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Name\"},\"id\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Id\"},\"example\":{\"type\":\"boolean\",\"title\":\"Example\",\"default\":false},\"tool_calls\":{\"items\":{\"$ref\":\"#\/components\/schemas\/ToolCall\"},\"type\":\"array\",\"title\":\"Tool Calls\",\"default\":[]},\"invalid_tool_calls\":{\"items\":{\"$ref\":\"#\/components\/schemas\/InvalidToolCall\"},\"type\":\"array\",\"title\":\"Invalid Tool Calls\",\"default\":[]},\"usage_metadata\":{\"anyOf\":[{\"$ref\":\"#\/components\/schemas\/UsageMetadata\"},{\"type\":\"null\"}]}},\"additionalProperties\":true,\"type\":\"object\",\"required\":[\"content\"],\"title\":\"AIMessage\",\"description\":\"Message from an AI.\\n\\nAIMessage is returned from a chat model as a response to a prompt.\\n\\nThis message represents the output of the model and consists of both\\nthe raw output as returned by the model together standardized fields\\n(e.g., tool calls, usage metadata) added by the LangChain framework.\"},\"Feedback\":{\"properties\":{\"score\":{\"anyOf\":[{\"type\":\"integer\"},{\"type\":\"number\"}],\"title\":\"Score\"},\"text\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Text\",\"default\":\"\"},\"run_id\":{\"type\":\"string\",\"title\":\"Run Id\"},\"log_type\":{\"type\":\"string\",\"const\":\"feedback\",\"title\":\"Log Type\",\"default\":\"feedback\"},\"service_name\":{\"type\":\"string\",\"const\":\"test-chatbot\",\"title\":\"Service Name\",\"default\":\"test-chatbot\"}},\"type\":\"object\",\"required\":[\"score\",\"run_id\"],\"title\":\"Feedback\",\"description\":\"Represents feedback for a conversation.\"},\"HTTPValidationError\":{\"properties\":{\"detail\":{\"items\":{\"$ref\":\"#\/components\/schemas\/ValidationError\"},\"type\":\"array\",\"title\":\"Detail\"}},\"type\":\"object\",\"title\":\"HTTPValidationError\"},\"HumanMessage\":{\"properties\":{\"content\":{\"anyOf\":[{\"type\":\"string\"},{\"items\":{\"anyOf\":[{\"type\":\"string\"},{\"additionalProperties\":true,\"type\":\"object\"}]},\"type\":\"array\"}],\"title\":\"Content\"},\"additional_kwargs\":{\"additionalProperties\":true,\"type\":\"object\",\"title\":\"Additional Kwargs\"},\"response_metadata\":{\"additionalProperties\":true,\"type\":\"object\",\"title\":\"Response Metadata\"},\"type\":{\"type\":\"string\",\"const\":\"human\",\"title\":\"Type\",\"default\":\"human\"},\"name\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Name\"},\"id\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Id\"},\"example\":{\"type\":\"boolean\",\"title\":\"Example\",\"default\":false}},\"additionalProperties\":true,\"type\":\"object\",\"required\":[\"content\"],\"title\":\"HumanMessage\",\"description\":\"Message from a human.\\n\\nHumanMessages are messages that are passed in from a human to the model.\\n\\nExample:\\n\\n    .. code-block:: python\\n\\n        from langchain_core.messages import HumanMessage, SystemMessage\\n\\n        messages = [\\n            SystemMessage(\\n                content=\\\"You are a helpful assistant! Your name is Bob.\\\"\\n            ),\\n            HumanMessage(\\n                content=\\\"What is your name?\\\"\\n            )\\n        ]\\n\\n        # Instantiate a chat model and invoke it with the messages\\n        model = ...\\n        print(model.invoke(messages))\"},\"InputChat\":{\"properties\":{\"messages\":{\"items\":{\"oneOf\":[{\"$ref\":\"#\/components\/schemas\/HumanMessage\"},{\"$ref\":\"#\/components\/schemas\/AIMessage\"},{\"$ref\":\"#\/components\/schemas\/ToolMessage\"}],\"discriminator\":{\"propertyName\":\"type\",\"mapping\":{\"ai\":\"#\/components\/schemas\/AIMessage\",\"human\":\"#\/components\/schemas\/HumanMessage\",\"tool\":\"#\/components\/schemas\/ToolMessage\"}}},\"type\":\"array\",\"title\":\"Messages\",\"description\":\"The chat messages representing the current conversation.\"}},\"type\":\"object\",\"required\":[\"messages\"],\"title\":\"InputChat\",\"description\":\"Represents the input for a chat session.\"},\"InputTokenDetails\":{\"properties\":{\"audio\":{\"type\":\"integer\",\"title\":\"Audio\"},\"cache_creation\":{\"type\":\"integer\",\"title\":\"Cache Creation\"},\"cache_read\":{\"type\":\"integer\",\"title\":\"Cache Read\"}},\"type\":\"object\",\"title\":\"InputTokenDetails\",\"description\":\"Breakdown of input token counts.\\n\\nDoes *not* need to sum to full input token count. Does *not* need to have all keys.\\n\\nExample:\\n\\n    .. code-block:: python\\n\\n        {\\n            \\\"audio\\\": 10,\\n            \\\"cache_creation\\\": 200,\\n            \\\"cache_read\\\": 100,\\n        }\\n\\n.. versionadded:: 0.3.9\\n\\nMay also hold extra provider-specific keys.\"},\"InvalidToolCall\":{\"properties\":{\"name\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Name\"},\"args\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Args\"},\"id\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Id\"},\"error\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Error\"},\"type\":{\"type\":\"string\",\"const\":\"invalid_tool_call\",\"title\":\"Type\"}},\"type\":\"object\",\"required\":[\"name\",\"args\",\"id\",\"error\"],\"title\":\"InvalidToolCall\",\"description\":\"Allowance for errors made by LLM.\\n\\nHere we add an `error` key to surface errors made during generation\\n(e.g., invalid JSON arguments.)\"},\"OutputTokenDetails\":{\"properties\":{\"audio\":{\"type\":\"integer\",\"title\":\"Audio\"},\"reasoning\":{\"type\":\"integer\",\"title\":\"Reasoning\"}},\"type\":\"object\",\"title\":\"OutputTokenDetails\",\"description\":\"Breakdown of output token counts.\\n\\nDoes *not* need to sum to full output token count. Does *not* need to have all keys.\\n\\nExample:\\n\\n    .. code-block:: python\\n\\n        {\\n            \\\"audio\\\": 10,\\n            \\\"reasoning\\\": 200,\\n        }\\n\\n.. versionadded:: 0.3.9\"},\"Request\":{\"properties\":{\"input\":{\"$ref\":\"#\/components\/schemas\/InputChat\"},\"config\":{\"anyOf\":[{\"$ref\":\"#\/components\/schemas\/RunnableConfig\"},{\"type\":\"null\"}]}},\"type\":\"object\",\"required\":[\"input\"],\"title\":\"Request\",\"description\":\"Represents the input for a chat request with optional configuration.\\n\\nAttributes:\\n    input: The chat input containing messages and other chat-related data\\n    config: Optional configuration for the runnable, including tags, callbacks, etc.\"},\"RunnableConfig\":{\"properties\":{\"tags\":{\"items\":{\"type\":\"string\"},\"type\":\"array\",\"title\":\"Tags\"},\"metadata\":{\"additionalProperties\":true,\"type\":\"object\",\"title\":\"Metadata\"},\"callbacks\":{\"anyOf\":[{\"items\":{},\"type\":\"array\"},{},{\"type\":\"null\"}],\"title\":\"Callbacks\"},\"run_name\":{\"type\":\"string\",\"title\":\"Run Name\"},\"max_concurrency\":{\"anyOf\":[{\"type\":\"integer\"},{\"type\":\"null\"}],\"title\":\"Max Concurrency\"},\"recursion_limit\":{\"type\":\"integer\",\"title\":\"Recursion Limit\"},\"configurable\":{\"additionalProperties\":true,\"type\":\"object\",\"title\":\"Configurable\"},\"run_id\":{\"anyOf\":[{\"type\":\"string\",\"format\":\"uuid\"},{\"type\":\"null\"}],\"title\":\"Run Id\"}},\"type\":\"object\",\"title\":\"RunnableConfig\",\"description\":\"Configuration for a Runnable.\"},\"ToolCall\":{\"properties\":{\"name\":{\"type\":\"string\",\"title\":\"Name\"},\"args\":{\"additionalProperties\":true,\"type\":\"object\",\"title\":\"Args\"},\"id\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Id\"},\"type\":{\"type\":\"string\",\"const\":\"tool_call\",\"title\":\"Type\"}},\"type\":\"object\",\"required\":[\"name\",\"args\",\"id\"],\"title\":\"ToolCall\",\"description\":\"Represents a request to call a tool.\\n\\nExample:\\n\\n    .. code-block:: python\\n\\n        {\\n            \\\"name\\\": \\\"foo\\\",\\n            \\\"args\\\": {\\\"a\\\": 1},\\n            \\\"id\\\": \\\"123\\\"\\n        }\\n\\n    This represents a request to call the tool named \\\"foo\\\" with arguments {\\\"a\\\": 1}\\n    and an identifier of \\\"123\\\".\"},\"ToolMessage\":{\"properties\":{\"content\":{\"anyOf\":[{\"type\":\"string\"},{\"items\":{\"anyOf\":[{\"type\":\"string\"},{\"additionalProperties\":true,\"type\":\"object\"}]},\"type\":\"array\"}],\"title\":\"Content\"},\"additional_kwargs\":{\"additionalProperties\":true,\"type\":\"object\",\"title\":\"Additional Kwargs\"},\"response_metadata\":{\"additionalProperties\":true,\"type\":\"object\",\"title\":\"Response Metadata\"},\"type\":{\"type\":\"string\",\"const\":\"tool\",\"title\":\"Type\",\"default\":\"tool\"},\"name\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Name\"},\"id\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"null\"}],\"title\":\"Id\"},\"tool_call_id\":{\"type\":\"string\",\"title\":\"Tool Call Id\"},\"artifact\":{\"title\":\"Artifact\"},\"status\":{\"type\":\"string\",\"enum\":[\"success\",\"error\"],\"title\":\"Status\",\"default\":\"success\"}},\"additionalProperties\":true,\"type\":\"object\",\"required\":[\"content\",\"tool_call_id\"],\"title\":\"ToolMessage\",\"description\":\"Message for passing the result of executing a tool back to a model.\\n\\nToolMessages contain the result of a tool invocation. Typically, the result\\nis encoded inside the `content` field.\\n\\nExample: A ToolMessage representing a result of 42 from a tool call with id\\n\\n    .. code-block:: python\\n\\n        from langchain_core.messages import ToolMessage\\n\\n        ToolMessage(content='42', tool_call_id='call_Jja7J89XsjrOLA5r!MEOW!SL')\\n\\n\\nExample: A ToolMessage where only part of the tool output is sent to the model\\n    and the full output is passed in to artifact.\\n\\n    .. versionadded:: 0.2.17\\n\\n    .. code-block:: python\\n\\n        from langchain_core.messages import ToolMessage\\n\\n        tool_output = {\\n            \\\"stdout\\\": \\\"From the graph we can see that the correlation between x and y is ...\\\",\\n            \\\"stderr\\\": None,\\n            \\\"artifacts\\\": {\\\"type\\\": \\\"image\\\", \\\"base64_data\\\": \\\"\/9j\/4gIcSU...\\\"},\\n        }\\n\\n        ToolMessage(\\n            content=tool_output[\\\"stdout\\\"],\\n            artifact=tool_output,\\n            tool_call_id='call_Jja7J89XsjrOLA5r!MEOW!SL',\\n        )\\n\\nThe tool_call_id field is used to associate the tool call request with the\\ntool call response. This is useful in situations where a chat model is able\\nto request multiple tool calls in parallel.\"},\"UsageMetadata\":{\"properties\":{\"input_tokens\":{\"type\":\"integer\",\"title\":\"Input Tokens\"},\"output_tokens\":{\"type\":\"integer\",\"title\":\"Output Tokens\"},\"total_tokens\":{\"type\":\"integer\",\"title\":\"Total Tokens\"},\"input_token_details\":{\"$ref\":\"#\/components\/schemas\/InputTokenDetails\"},\"output_token_details\":{\"$ref\":\"#\/components\/schemas\/OutputTokenDetails\"}},\"type\":\"object\",\"required\":[\"input_tokens\",\"output_tokens\",\"total_tokens\"],\"title\":\"UsageMetadata\",\"description\":\"Usage metadata for a message, such as token counts.\\n\\nThis is a standard representation of token usage that is consistent across models.\\n\\nExample:\\n\\n    .. code-block:: python\\n\\n        {\\n            \\\"input_tokens\\\": 350,\\n            \\\"output_tokens\\\": 240,\\n            \\\"total_tokens\\\": 590,\\n            \\\"input_token_details\\\": {\\n                \\\"audio\\\": 10,\\n                \\\"cache_creation\\\": 200,\\n                \\\"cache_read\\\": 100,\\n            },\\n            \\\"output_token_details\\\": {\\n                \\\"audio\\\": 10,\\n                \\\"reasoning\\\": 200,\\n            }\\n        }\\n\\n.. versionchanged:: 0.3.9\\n\\n    Added ``input_token_details`` and ``output_token_details``.\"},\"ValidationError\":{\"properties\":{\"loc\":{\"items\":{\"anyOf\":[{\"type\":\"string\"},{\"type\":\"integer\"}]},\"type\":\"array\",\"title\":\"Location\"},\"msg\":{\"type\":\"string\",\"title\":\"Message\"},\"type\":{\"type\":\"string\",\"title\":\"Error Type\"}},\"type\":\"object\",\"required\":[\"loc\",\"msg\",\"type\"],\"title\":\"ValidationError\"}}}}\"\r\n  \"api_endpoint\": \"\/stream_messages",
        "chatbot_name": "AutomationChatBoat"
    }

    context.response = requests.put(context.url, headers=context.headers, json=payload)
    logging.info(f"PUT request for non-existent chatbot ID response: {context.response.text}")
    print(f"PUT request for non-existent chatbot ID response: {context.response.text}")


@when(u'the user receives the chatbot API update response')
def step_impl(context):
    assert_that(context.response).is_not_none()

@then(u'the status code returned should be 200 for successful update')
def step_impl(context):
    assert_that(context.response.status_code).is_equal_to(200)


@then(u'the response should contain a valid chatbotID')
def step_impl(context):
    response_json = context.response2.json()
    assert_that(response_json.get("chatbot_id")).is_equal_to(context.chatbot_id)



@then(u'the response should contain a "status" equal to "API_updated"')
def step_impl(context):
    response_json = context.response2.json()
    assert_that(response_json.get("status")).is_equal_to("API_updated")


@then(u'should be 404 for not found error')
def step_impl(context):
    assert_that(context.response.status_code).is_equal_to(404)

@then(u'should error message "Not Found"')
def step_impl(context):
    error_message = context.response.json().get("error")
    assert_that(error_message).is_equal_to("Not Found")

@then(u'the message should contain "Chatbot with ID {chatbot_id} not found."')
def step_impl(context, chatbot_id):
    expected_message = f"Chatbot with ID {chatbot_id} not found."
    actual_message = context.response.json().get("message")
    assert_that(actual_message).is_equal_to(expected_message)


import requests
import logging
from behave import given, when, then
from assertpy import assert_that
from utilities.configurations import getConfig

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


########################### Scenario Outline: SQL injection attempt in the Update Chatbot API request ###########################

@given(
    u'User send request to update API "{chatbot_id}" with environment ID "{env_id}" and endpoint "{chatbot_url}"')
def step_impl(context, chatbot_id, env_id, chatbot_url):
    """Send PUT request to update chatbot API details with malicious SQL injection payload"""

    config = getConfig()
    base_url = config['API']['BaseURL']
    api_key = config['API']['APIKey']

    context.url = f"{base_url}/chatbots/{chatbot_id}/api"
    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    # Prepare the malicious SQL injection payload
    payload = {
        "chatbot_id": chatbot_id,
        "env_id": env_id,
        "chatbot_url": chatbot_url,
        "api_endpoint": "' OR 1=1 --",  # SQL injection in api_endpoint
        "api_specifications": "' OR 1=1 --",  # SQL injection in api_specifications
    }

    # Send the PUT request with SQL injection input
    context.response = requests.put(context.url, json=payload, headers=context.headers)
    logger.info(f"SQL Injection PUT Request Response: {context.response.text}")
    print(f"SQL Injection PUT Request Response: {context.response.text}")


@when(u'the user receives the API response')
def step_impl(context):
    """The response is already captured in context.response during the PUT request"""
    assert_that(context.response).is_not_none()


@then(u'message should contain "Invalid input:"')
def step_impl(context):
    """Verify that the response contains 'Invalid input:' indicating the input is invalid"""
    response_json = context.response.json()
    logger.info(f"Expected error message: 'Invalid input:', Got: {response_json.get('message')}")
    assert_that(response_json.get("message")).contains("Invalid input:")


@then(u'the message should contain "chatbot_id" with validation errors related to the input')
def step_impl(context):
    """Verify that the response contains validation errors related to chatbot_id"""
    response_json = context.response.json()
    logger.info(f"Expected validation errors for 'chatbot_id', Got: {response_json.get('error')}")
    assert_that(response_json.get("error")).contains("Bad Request")
