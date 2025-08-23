import requests
import logging
from behave import given, when, then
from assertpy import assert_that
from utilities.configurations import getConfig

# Set up logging to print out the response in the console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

########################### Scenario: Verify PUT request successfully updates chatbot details ###########################

@given(u'User sends PUT request to update chatbot details with chatbot_id "{chatbot_id}", chatbot_name "{chatbot_name}", chatbot_description "{chatbot_description}", and env_id "{env_id}"')
def step_impl(context, chatbot_id, chatbot_name, chatbot_description, env_id):
    """Send PUT request to update chatbot details for a given chatbot_id, chatbot_name, chatbot_description, and env_id"""
    config = getConfig()
    context.url = f"{config['API']['BaseURL']}/chatbots/{chatbot_id}"

    # Fetch the API key from the configuration
    api_key = config['API']['APIKey']  # API key fetched from the config file

    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    # Request Body
    context.request_body = {
        "chatbot_id": chatbot_id,
        "chatbot_name": chatbot_name,
        "chatbot_description": chatbot_description,
        "env_id": env_id
    }

    # Send the PUT request to update the chatbot details
    context.response = requests.put(context.url, json=context.request_body, headers=context.headers)

    # Log the PUT request response
    logger.info(f"PUT Chatbot API Response: {context.response.text}")
    print(f"PUT Chatbot API Response: {context.response.text}")  # Fallback to print in console



@then(u'the response should contain the chatbot_id')
def step_impl(context):
    """Verify that the response contains the chatbot_id"""
    response_json = context.response.json()
    logger.info(f"Response contains chatbot_id: {response_json.get('chatbot_id')}")
    assert_that(response_json).contains("chatbot_id")

@then(u'the status should be In_progress')
def step_impl(context):
    """Verify that the status is 'In_progress' in the response"""
    response_json = context.response.json()
    logger.info(f"Response status: {response_json.get('status')}")
    assert_that(response_json['status']).is_equal_to("In_progress")

@then(u'the status code returned should be 400')
def step_impl(context):
    """Verify that the status code is 400 for a bad request"""
    assert_that(context.response.status_code).is_equal_to(400)

@then(u'the response should contain error variable with value Bad Request')
def step_impl(context):
    """Verify that the response contains an error variable with 'Bad Request'"""
    response_json = context.response.json()
    logger.info(f"Response contains error: {response_json.get('error')}")
    assert_that(response_json).contains("error")
    assert_that(response_json['error']).is_equal_to("Bad Request")

@then(u'the response should contain the The chatbot must be in AVAILABLE status')
def step_impl(context):
    """Verify that the response contains the message 'The chatbot must be in AVAILABLE status'"""
    response_json = context.response.json()
    logger.info(f"Response message: {response_json.get('message')}")
    assert_that(response_json['message']).contains("The chatbot must be in AVAILABLE status")
