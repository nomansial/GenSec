import requests
import logging
from behave import given, when, then
from assertpy import assert_that
from utilities.configurations import getConfig
from Delete_an_environment_and_associated_data import step_impl  # Importing shared steps

# Set up logging to print out the response in the console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

########################### Scenario Outline: Verify Get Chatbot API retrieves chatbots successfully ###########################

@given(u'User sends GET request to fetch chatbots with env_id "{env_id}"')
def step_impl(context, env_id):
    """Send GET request to fetch chatbots for a given env_id"""
    config = getConfig()
    context.url = f"{config['API']['BaseURL']}/chatbots?env_id={env_id}"

    # Fetch the API key from the configuration
    api_key = config['API']['APIKey']  # API key fetched from the config file

    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    # Send the GET request to fetch chatbots
    context.response = requests.get(context.url, headers=context.headers)

    # Log the Get Chatbot API response
    logger.info(f"Get Chatbot API Response: {context.response.text}")
    print(f"Get Chatbot API Response: {context.response.text}")  # Fallback to print in console


@then(u'the status code returned should be 200 for a successful request')
def step_impl(context):
    """Verify that the status code for the GET request is 200"""
    logger.info(f"Expected Status Code: 200, Got: {context.response.status_code}")
    assert_that(context.response.status_code).is_equal_to(200)


@then(u'the response should contain a "chatbots" array')
def step_impl(context):
    """Verify that the response contains a 'chatbots' array"""
    response_json = context.response.json()
    logger.info(f"Response contains 'chatbots': {response_json.get('chatbots')}")
    assert_that(response_json).contains("chatbots")


@then(u'the "chatbots" array should contain at least one chatbot')
def step_impl(context):
    """Verify that the 'chatbots' array contains at least one chatbot"""
    response_json = context.response.json()
    chatbots = response_json.get("chatbots")
    logger.info(f"Number of chatbots: {len(chatbots)}")
    assert_that(len(chatbots)).is_greater_than(0)


@then(u'the response should contain chatbot details including "chatbot_id" and "name"')
def step_impl(context):
    """Verify that the response contains 'chatbot_id' and 'name', and check their length"""
    response_json = context.response.json()
    chatbots = response_json.get("chatbots")

    for chatbot in chatbots:
        chatbot_id = chatbot.get("chatbot_id")
        chatbot_name = chatbot.get("name")

        logger.info(f"Chatbot ID: {chatbot_id}, Name: {chatbot_name}")

        # Check that chatbot_id and name are not null or empty
        assert_that(chatbot_id).is_not_none().is_length(36)  # Check length of the ID (UUID format)
        assert_that(chatbot_name).is_not_none()  # Ensure name is not empty

    logger.info("All chatbots have valid chatbot_id and name.")

########################### Negative Scenario: Verify Get Chatbot API when the env_id is invalid or missing ###########################


@then(u'error code should be 400 for bad request error')
def step_impl(context):
    """Verify that the status code for the error is 400"""
    logger.info(f"Expected Status Code: 400, Got: {context.response.status_code}")
    assert_that(context.response.status_code).is_equal_to(400)


@then(u'response shows error message "Bad Request"')
def step_impl(context):
    """Verify that the response contains 'Bad Request' error message"""
    response_json = context.response.json()
    logger.info(f"Expected error message: 'Bad Request', Got: {response_json.get('error')}")
    assert_that(response_json.get("error")).is_equal_to("Bad Request")


@then(u'the message should be "Invalid input:"')
def step_impl(context):
    """Verify that the error message contains 'Invalid input:'"""
    response_json = context.response.json()
    logger.info(f"Expected error message: 'Invalid input:', Got: {response_json.get('message')}")
    assert_that(response_json.get("message")).contains("Invalid input:")
