import requests
import logging
from behave import given, when, then
from assertpy import assert_that

from utilities.configurations import getConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@given(u'User sends GET request to fetch customer API key')
def step_impl(context):
    """Send GET request to fetch customer API key"""
    config = getConfig()
    context.url = f"{config['API']['BaseURL']}/customers/me/api"
    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': "AIzaSyCNI5CQeoAAfvQB07m2KGqDXLlgQKMg-aM"
    }

    # Send GET request
    context.response = requests.get(context.url, headers=context.headers)

    # Log response
    logger.info(f"Get Customer API Key Response: {context.response.text}")
    print(f"Get Customer API Key Response: {context.response.text}")

@then(u'the status code returned should be 200 for a successful request for get customer API')
def step_impl(context):
    """Verify status code 200"""
    assert_that(context.response.status_code).is_equal_to(200)

@then(u'the response should contain the customer API key details')
def step_impl(context):
    """Verify response contains key details"""
    response_json = context.response.json()
    logger.info(f"Response contains customer API key details: {response_json}")
    assert_that(response_json).contains("key_creation_timestamp")
    assert_that(response_json).contains("truncated_key")

@then(u'all the parameters in the response should not be None')
def step_impl(context):
    """Ensure parameters are not None"""
    response_json = context.response.json()
    expected_params = ["key_creation_timestamp", "truncated_key"]

    for param in expected_params:
        param_value = response_json.get(param)
        logger.info(f"Checking parameter: {param} - Value: {param_value}")
        assert_that(param_value).is_not_none()

    logger.info("All parameters in customer API key response are valid.")

@given(u'User sends GET request to fetch customer API key with invalid or missing API key')
def step_impl(context):
    """Send GET request without API key"""
    config = getConfig()
    context.url = f"{config['API']['BaseURL']}/customers/me/api"
    context.headers = {
        'Content-Type': 'application/json'
        # API key is intentionally missing/invalid
    }

    context.response = requests.get(context.url, headers=context.headers)
    logger.info(f"Get Customer API Key (Invalid/Missing Key) Response: {context.response.text}")
    print(f"Get Customer API Key (Invalid/Missing Key) Response: {context.response.text}")

@then(u'the status code returned should be 401 for unauthorized request')
def step_impl(context):
    """Verify status code 401"""
    assert_that(context.response.status_code).is_equal_to(401)

@then(u'the response should contain an error message for customer API')
def step_impl(context):
    """Verify error message exists"""
    response_json = context.response.json()
    assert_that(response_json).contains("message")
    assert_that(response_json).contains("code")

@then(u'the error message should state "Invalid or missing API key"')
def step_impl(context):
    """Verify specific unauthorized error message"""
    response_json = context.response.json()
    expected_msg = "UNAUTHENTICATED: Method doesn't allow unregistered callers"
    assert_that(response_json["message"]).contains(expected_msg)
    assert_that(response_json["code"]).is_equal_to(401)
    logger.info(f"Unauthorized error validated: {response_json}")
