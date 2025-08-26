import time

import requests
from behave import given, when, then
from assertpy import assert_that
from utilities.configurations import getConfig


# Step to fetch env_id from Create Environment API
@given(u'User fetches env_id from Create Environment API')
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
    time.sleep(2)
    # Check if the status code is 200 for create
    assert_that(context.response.status_code).is_equal_to(200)

    # Extract the env_id from the response and store it in context
    response_json = context.response.json()
    context.env_id = response_json.get("env_id")
    assert_that(context.env_id).is_not_none().is_not_empty()


# Step to send DELETE API request using the fetched env_id
@when(u'user sends delete API call')
def step_impl(context):
    """Send DELETE request to delete the environment with the fetched env_id"""
    config = getConfig()
    context.url = f"{config['API']['BaseURL']}/environments/{context.env_id}"

    api_key = config['API'].get('APIKey', '')  # Correct API key from config

    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    # Send the DELETE request
    context.response2 = requests.delete(context.url, headers=context.headers)
    time.sleep(2)


# Step to verify the status code for the DELETE request
@then(u'the status code returned should be 200 for the delete environment')
def step_impl(context):
    """Verify that the status code for the delete environment API is 200"""
    actual_status_code = context.response2.status_code
    assert_that(actual_status_code).is_equal_to(200)


# Step to verify the status in the response is "Deleted"
@then(u'contain a "status" of "Deleted"')
def step_impl(context):
    """Verify that the response contains the status 'Deleted'"""
    response_json = context.response2.json()
    assert_that(response_json.get("status")).is_equal_to("Deleted")


# Step to verify the correct env_id is returned
@then(u'contain the correct "env_id"')
def step_impl(context):
    """Verify that the response contains the correct 'env_id'"""
    response_json = context.response2.json()
    assert_that(response_json.get("env_id")).is_equal_to(context.env_id)


# Step to verify that the response contains a non-null 'name'
@then(u'should have a non-null "name"')
def step_impl(context):
    """Verify that the response contains a non-null 'name'"""
    response_json = context.response2.json()
    assert_that(response_json.get("name")).is_not_none().is_not_empty()
