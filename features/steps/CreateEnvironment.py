import requests
from behave import given, when, then
from assertpy import assert_that
from utilities.configurations import getConfig


@given(u'the user provides the environment details "{env_name}" and "{env_description}"')
def step_impl(context, env_name, env_description):
    """Prepare request payload for positive or negative case"""
    config = getConfig()
    context.url = f"{config['API']['BaseURL']}/environments"

    # Read API key from config
    api_key = config['API'].get('APIKey', '')

    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    # Convert 'None' placeholder to empty string
    env_name = env_name.strip('"')
    env_description = env_description.strip('"')
    if env_name.lower() == "none":
        env_name = ""
    if env_description.lower() == "none":
        env_description = ""

    context.request_payload = {
        "env_name": env_name,
        "env_description": env_description
    }


@when(u'the user sends a request to create the environment')
def step_impl(context):
    """Send POST request"""
    context.response = requests.post(
        context.url,
        json=context.request_payload,
        headers=context.headers
    )


@then(u''
      u'code should be {status_code:d}')
def step_impl(context, status_code):
    """Generic status code check"""
    actual_status_code = context.response.status_code
    assert_that(actual_status_code).is_equal_to(status_code)


@then(u'the response should be validated based on error_message {error_message}')
def step_impl(context, error_message):
    """Validate either env_id (positive) or error_message (negative)"""
    # Convert 'None' placeholder to empty string
    if error_message.strip().lower() == "none":
        error_message = ""

    # Print API response for debugging
    print("\n--- API Response ---")
    print(context.response.text)
    print("-------------------\n")

    # Parse JSON safely
    try:
        response_json = context.response.json()
    except ValueError:
        response_json = {}

    if not error_message:
        # Positive case: validate env_id
        assert_that("env_id" in response_json).is_true()
        assert_that(response_json["env_id"]).is_not_empty()
    else:
        # Negative case: validate error message
        assert_that("error" in response_json).is_true()
        if isinstance(response_json["error"], dict) and "message" in response_json["error"]:
            actual_error = response_json["error"]["message"]
        else:
            actual_error = response_json["error"]
        assert_that(actual_error).contains(error_message)
