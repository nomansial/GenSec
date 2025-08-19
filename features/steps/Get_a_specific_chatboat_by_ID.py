import requests
import logging
from behave import given, when, then
from assertpy import assert_that
from utilities.configurations import getConfig

# Set up logging to print out the response in the console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

########################### Scenario: Verify Get Chatbot API retrieves chatbot details ###########################

@given(u'User sends GET request to fetch chatbot details with chatbot_id "{chatbot_id}"')
def step_impl(context, chatbot_id):
    """Send GET request to fetch chatbot details for a given chatbot_id"""
    config = getConfig()
    context.url = f"{config['API']['BaseURL']}/chatbots/{chatbot_id}"

    # Fetch the API key from the configuration
    api_key = config['API']['APIKey']  # API key fetched from the config file

    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    # Send the GET request to fetch chatbot details
    context.response = requests.get(context.url, headers=context.headers)

    # Log the Get Chatbot API response
    logger.info(f"Get Chatbot API Response: {context.response.text}")
    print(f"Get Chatbot API Response: {context.response.text}")  # Fallback to print in console



@then(u'the response should contain the chatbot details')
def step_impl(context):
    """Verify that the response contains chatbot details"""
    response_json = context.response.json()
    logger.info(f"Response contains chatbot details: {response_json}")
    assert_that(response_json).contains("chatbot_id")
    assert_that(response_json).contains("name")
    assert_that(response_json).contains("api_endpoint")
    assert_that(response_json).contains("api_secret_location")
    assert_that(response_json).contains("status")
    assert_that(response_json).contains("env_id")


@then(u'all the parameters in the response should not be None except for api_specifications')
def step_impl(context):
    """Verify that none of the parameters in the response are None"""
    response_json = context.response.json()

    # List of all the expected parameters
    expected_params = [
        "chatbot_id",
        "name",
        "api_endpoint",
        "api_secret_location",
        "associated_abuse_cases",
        "chatbot_id",
        "creation_timestamp",
        "env_id",
        "json",
        "last_update_timestamp",
        "similar_known_use_cases",
        "status",
        "url"
    ]

    # Loop through each parameter and check that it is not None
    for param in expected_params:
        param_value = response_json.get(param)
        logger.info(f"Checking parameter: {param} - Value: {param_value}")
        assert_that(param_value).is_not_none()

    logger.info("All parameters have valid values (not None).")

@then(u'the status code returned should be 400 for a bad request')
def step_impl(context):
    """Verify that the status code is 400 for invalid chatbot_id"""
    assert_that(context.response.status_code).is_equal_to(400)


@then(u'the error message should state "Invalid input" with a specific message for chatbot_id')
def step_impl(context):
    """Verify that the error message contains 'Invalid input' for chatbot_id"""
    response_json = context.response.json()
    assert_that(response_json['message']).contains("Invalid input")


@then(u'the status code returned should be 404 for "Not Found"')
def step_impl(context):
    """Verify that the status code is 404 when chatbot is not found"""
    assert_that(context.response.status_code).is_equal_to(404)


@then(u'the error message should state Chatbot with ID not found.')
def step_impl(context):
    """Verify that the error message contains 'Chatbot with ID' and 'Not Found'"""
    response_json = context.response.json()

    # Check if the error contains 'Not Found' and the message contains 'Chatbot with ID'
    assert_that(response_json['error']).contains("Not Found")
    assert_that(response_json['message']).contains("Chatbot with ID")
    logger.info(response_json)

