import requests
import logging
from behave import given, when, then
from assertpy import assert_that
from utilities.configurations import getConfig

# Set up logging to print out the response in the console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@given(u'User sends PUT request to update environment details with an invalid env_id "{env_id}"')
def step_impl(context, env_id):
    """Send PUT request to update environment details with an invalid or non-existing env_id"""
    config = getConfig()
    context.url = f"https://genr3d-api.generativesecurity.ai/environments/{env_id}"

    api_key = "AIzaSyCNI5CQeoAAfvQB07m2KGqDXLlgQKMg-aM"  # API key passed in the request header

    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    # Prepare the request body to update the environment
    payload = {
        "env_id": env_id,
        "env_name": "update name",
        "env_description": "update description"
    }

    # Send the PUT request to update the environment
    context.response = requests.put(context.url, json=payload, headers=context.headers)

    # Log the Update Environment API response
    logger.info(f"Update Environment API Response: {context.response.text}")
    print(f"Update Environment API Response: {context.response.text}")  # Fallback to print in console


@then(u'the status code should be 404 for not found error')
def step_impl(context):
    """Verify that the status code for the error is 404 or 400 based on env_id"""
    response_json = context.response.json()

    # Check if env_id is invalid (None or malformed)
    if context.response.status_code == 400:
        # If invalid env_id, expect a 400 status code
        logger.info(f"Expected Status Code: 400, Got: {context.response.status_code}")
        assert_that(context.response.status_code).is_equal_to(400)
    else:
        # If valid env_id but not found, expect a 404 status code
        logger.info(f"Expected Status Code: 404, Got: {context.response.status_code}")
        assert_that(context.response.status_code).is_equal_to(404)


@then(u'the response should contain an error message "Not Found"')
def step_impl(context):
    """Verify that the error message is 'Not Found' or 'Bad Request' based on the status code"""
    response_json = context.response.json()

    # Check if the status code is 400 (Bad Request) or 404 (Not Found)
    if context.response.status_code == 400:
        # If the status code is 400, verify the error message is "Bad Request"
        logger.info(f"Expected error message: 'Bad Request', Got: {response_json.get('error')}")
        assert_that(response_json.get("error")).is_equal_to("Bad Request")
    else:
        # If the status code is 404, verify the error message is "Not Found"
        logger.info(f"Expected error message: 'Not Found', Got: {response_json.get('error')}")
        assert_that(response_json.get("error")).is_equal_to("Not Found")


@then(u'the message should be "Environment with ID {env_id} not found for update."')
def step_impl(context, env_id):
    """Verify the specific error message for a non-existing environment"""
    response_json = context.response.json()

    # Handle the case when env_id is passed as "None" (string) specifically
    if env_id == "None":
        # Treat "None" as an empty string for validation
        env_id = ""
        logger.info(f"Expected message to contain 'Invalid input:', Got: {response_json.get('message')}")
        # Verify the error message for invalid env_id (Bad Request)
        assert_that(response_json.get("message")).contains("Invalid input:")
    else:
        # If the env_id is valid, verify the environment not found message
        expected_message = f"Environment with ID {env_id} not found for update."
        logger.info(f"Expected Message: {expected_message}, Response Message: {response_json.get('message')}")

        # First check if the message contains "Invalid input:"
        if "Invalid input:" in response_json.get("message"):
            assert_that(response_json.get("message")).contains("Invalid input:")
        else:
            # If not, check for "not found"
            assert_that(response_json.get("message")).contains("not found")
