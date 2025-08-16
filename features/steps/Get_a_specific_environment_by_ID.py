import requests
import logging
from behave import given, when, then
from assertpy import assert_that
from utilities.configurations import getConfig
import re
from datetime import datetime

# Set up logging to print out the response in the console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Step to fetch env_id from Create Environment API
@given(u'take env_id from Create Environment API')
def step_impl(context):
    """Send POST request to create an environment and extract the env_id"""
    config = getConfig()
    context.url = f"{config['API']['BaseURL']}/environments"

    # Prepare the request payload for creating an environment
    payload = {
        "env_name": "Automation QA",
        "env_description": "System testing please ignore"
    }

    api_key = config['API'].get('APIKey', '')  # Correct API key from config

    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    # Send the POST request to create the environment
    context.response = requests.post(context.url, json=payload, headers=context.headers)

    # Log the Create Environment API response
    logger.info(f"Create Environment API Response: {context.response.text}")

    # Check if the status code is 200 for create
    assert_that(context.response.status_code).is_equal_to(200)

    # Extract the env_id from the response and store it in context
    response_json = context.response.json()
    context.env_id = response_json.get("env_id")
    assert_that(context.env_id).is_not_none().is_not_empty()


# Step to send GET request using the fetched env_id (Positive Scenario)
@when(u'user sends GET request to fetch environment details with valid env_id')
def step_impl(context):
    """Send GET request to fetch environment details using valid env_id from context"""
    config = getConfig()
    context.url = f"{config['API']['BaseURL']}/environments/{context.env_id}"  # Correct URL format

    api_key = config['API'].get('APIKey', '')  # Correct API key from config

    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    # Send the GET request to fetch the environment details
    context.response = requests.get(context.url, headers=context.headers)

    # Debugging: Print URL and headers for verification
    logger.info(f"Request URL: {context.url}")
    logger.info(f"Request Headers: {context.headers}")


# Positive Scenario Steps
@then(u'the status code should be 200 for the successful request')
def step_impl(context):
    """Verify that the status code for the GET request is 200"""
    logger.info(f"Expected Status Code: 200, Got: {context.response.status_code}")
    assert_that(context.response.status_code).is_equal_to(200)


@then(u'the response should contain the env_id')
def step_impl(context):
    """Verify that the env_id in the response matches the env_id fetched from Create Environment API"""
    response_json = context.response.json()
    # Compare the env_id from the GET request response with the env_id from the Create Environment API
    logger.info(f"Expected env_id: {context.env_id}, Response env_id: {response_json.get('env_id')}")
    assert_that(response_json.get("env_id")).is_equal_to(context.env_id)



@then(u'the "env_id" should match the env_id fetched from Create Environment API')
def step_impl(context):
    """Verify that the env_id in the response matches the env_id fetched from the Create Environment API"""
    response_json = context.response.json()
    logger.info(f"Expected env_id: {context.env_id}, Response env_id: {response_json.get('env_id')}")
    assert_that(response_json.get("env_id")).is_equal_to(context.env_id)


@then(u'the "creation_timestamp" should be in the correct timestamp format (yyyy-MM-dd\'T\'HH:mm:ss\'Z\')')
def step_impl(context):
    """Verify that the creation timestamp is in the correct format"""
    response_json = context.response.json()
    creation_timestamp = response_json.get("creation_timestamp")
    timestamp_format = "%Y-%m-%dT%H:%M:%SZ"
    try:
        datetime.strptime(creation_timestamp, timestamp_format)
    except ValueError:
        assert_that(False).is_true()  # Fail if the format is not correct


@then(u'the "last_update_timestamp" should be in the correct timestamp format (yyyy-MM-dd\'T\'HH:mm:ss\'Z\')')
def step_impl(context):
    """Verify that the last update timestamp is in the correct format"""
    response_json = context.response.json()
    last_update_timestamp = response_json.get("last_update_timestamp")
    timestamp_format = "%Y-%m-%dT%H:%M:%SZ"
    try:
        datetime.strptime(last_update_timestamp, timestamp_format)
    except ValueError:
        assert_that(False).is_true()  # Fail if the format is not correct


@then(u'the "description" should not be null')
def step_impl(context):
    """Verify that the description is not null or empty"""
    response_json = context.response.json()
    description = response_json.get("description")
    assert_that(description).is_not_none().is_not_empty()


@then(u'the "name" should not be null')
def step_impl(context):
    """Verify that the name is not null"""
    response_json = context.response.json()
    name = response_json.get("name")
    assert_that(name).is_not_none().is_not_empty()


# Negative Scenario Steps
@given(u'User sends GET request to fetch environment details with an invalid or missing env_id "{env_id}"')
def step_impl(context, env_id):
    """Send GET request to fetch environment details using invalid env_id (non-existing or blank)"""
    config = getConfig()
    context.url = f"{config['API']['BaseURL']}/environments/{env_id}"

    api_key = config['API'].get('APIKey', '')  # Correct API key from config

    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    # Send the GET request to fetch the environment details
    context.response = requests.get(context.url, headers=context.headers)

@when(u'user receives the response')
def step_impl(context):
    """This step will handle the receiving of the response from the GET request"""
    # The response is already assigned in the previous given step, so no action needed here
    pass


@then(u'the status code should be 400 for not found error')
def step_impl(context):
    """Verify that the status code for the error is 404"""
    logger.info(f"Expected Status Code: 404, Got: {context.response.status_code}")
    assert_that(context.response.status_code).is_equal_to(400)


@then(u'the response should contain an error message')
def step_impl(context):
    """Verify that the error message is 'Not Found'"""
    response_json = context.response.json()
    assert_that(response_json.get("error")).is_equal_to("Bad Request")
