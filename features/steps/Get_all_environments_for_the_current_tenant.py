import requests
from behave import given, when, then
from assertpy import assert_that
from utilities.configurations import getConfig


@given(u'the user sends a GET request to retrieve the environments')
def step_impl(context):
    """Send GET request to retrieve the environments"""
    config = getConfig()
    context.url = f"{config['API']['BaseURL']}/environments"

    # Use the correct API key for the request
    api_key = config['API'].get('APIKey', '')  # Correct API key from config

    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key  # API key in header
    }

    context.response = requests.get(context.url, headers=context.headers)


@when(u'the user receives the response')
def step_impl(context):
    """This step is already handled by the GET request in the previous step."""
    pass


@then(u'the status code returned should be 200')
def step_impl(context):
    """Verify that the status code returned is 200"""
    actual_status_code = context.response.status_code
    assert_that(actual_status_code).is_equal_to(200)


@then(u'each environment should have a non-null "env_id" and "name"')
def step_impl(context):
    """Check that each environment has a non-null 'env_id' and 'name'"""
    try:
        response_json = context.response.json()
        environments = response_json.get("environments", [])

        for env in environments:
            assert_that(env.get("env_id")).is_not_none().is_not_empty()
            assert_that(env.get("name")).is_not_none().is_not_empty()
    except ValueError:
        assert False, "Failed to parse response JSON"
