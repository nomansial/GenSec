import time

import requests
from behave import given, when, then
from assertpy import assert_that

from utilities.authentication import get_firebase_id_token
from utilities.configurations import getConfig


# Step to fetch env_id from Create Environment API
@given(u'FireBase_User fetches env_id from Create Environment API')
def step_impl(context):
    """Send POST request to create an environment and extract the env_id"""
    config = getConfig()
    context.url = f"{config['API']['FireBaseURL']}/environments"

    # Prepare the request payload for creating an environment
    payload = {
        "env_name": "Automation QA",
        "env_description": "System testing please ignore"
    }

    # Get the Firebase idToken
    id_token = get_firebase_id_token()
    print(repr(id_token))
    #logger.info(f"Passing token like this: {id_token}")

    context.headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {id_token}'  # Use OAuth 2.0 Bearer token
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
@when(u'FireBase_user sends delete API call')
def step_impl(context):
    """Send DELETE request to delete the environment with the fetched env_id"""
    config = getConfig()
    context.url = f"{config['API']['FireBaseURL']}/environments/{context.env_id}"

    # Get the Firebase idToken
    id_token = get_firebase_id_token()
    print(repr(id_token))
    #logger.info(f"Passing token like this: {id_token}")

    context.headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {id_token}'  # Use OAuth 2.0 Bearer token
    }

    # Send the DELETE request
    context.response2 = requests.delete(context.url, headers=context.headers)
    time.sleep(2)


# Step to verify the status code for the DELETE request
@then(u'FireBase_the status code returned should be 200 for the delete environment')
def step_impl(context):
    """Verify that the status code for the delete environment API is 200"""
    actual_status_code = context.response2.status_code
    assert_that(actual_status_code).is_equal_to(200)


# Step to verify the status in the response is "Deleted"
@then(u'FireBase_contain a "status" of "Deleted"')
def step_impl(context):
    """Verify that the response contains the status 'Deleted'"""
    response_json = context.response2.json()
    assert_that(response_json.get("status")).is_equal_to("Deleted")


# Step to set an invalid env_id
@given(u'FireBase_User sets an invalid env_id')
def step_impl(context):
    """Set an invalid environment ID for deletion"""
    context.env_id = "bbd21bd8-bf14-4d34-b6f0-44400d057187"
    config = getConfig()
    context.url = f"{config['API']['FireBaseURL']}/environments/{context.env_id}"

    # Get the Firebase idToken
    id_token = get_firebase_id_token()
    print(repr(id_token))
    #logger.info(f"Passing token like this: {id_token}")

    context.headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {id_token}'  # Use OAuth 2.0 Bearer token
    }

# Step to verify the correct env_id is returned
@then(u'FireBase_contain the correct "env_id"')
def step_impl(context):
    """Verify that the response contains the correct 'env_id'"""
    response_json = context.response2.json()
    assert_that(response_json.get("env_id")).is_equal_to(context.env_id)


# Step to verify that the response contains a non-null 'name'
@then(u'FireBase_should have a non-null "name"')
def step_impl(context):
    """Verify that the response contains a non-null 'name'"""
    response_json = context.response2.json()
    assert_that(response_json.get("name")).is_not_none().is_not_empty()


# Step to send DELETE request with invalid env_id
@when(u'FireBase_delete API call is triggered')
def step_impl(context):
    """Send DELETE request with invalid env_id"""
    context.response = requests.delete(context.url, headers=context.headers)

# Step to verify error message in response
@then(u'FireBase_contain an error message "Environment not found"')
def step_impl(context):
    """Verify error message for invalid env_id"""
    response_json = context.response.json()
    assert_that(response_json.get("error")).is_equal_to("Not Found")


# Step to set a malicious env_id for injection attack
@given(u'FireBase_User sets a malicious env_id for injection attack')
def step_impl(context):
    """Set a malicious env_id to simulate injection attack"""
    context.env_id = "123'; DROP TABLE environments;--"
    config = getConfig()
    context.url = f"{config['API']['FireBaseURL']}/environments/{context.env_id}"

    # Get the Firebase idToken
    id_token = get_firebase_id_token()
    print(repr(id_token))
    #logger.info(f"Passing token like this: {id_token}")

    context.headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {id_token}'  # Use OAuth 2.0 Bearer token
    }


# Step to send DELETE request with malicious env_id
@when(u'FireBase_user sends delete API call for security scenrio')
def step_impl(context):
    """Send DELETE request with malicious env_id"""
    context.response = requests.delete(context.url, headers=context.headers)


# Step to verify error contains "Bad Request"
@then(u'FireBase_error contains "Bad Request"')
def step_impl(context):
    """Verify that the error message contains 'Bad Request'"""
    response_json = context.response.json()
    assert_that(response_json.get("error")).is_equal_to("Bad Request")
    assert_that(response_json.get("message")).contains("Invalid input")


