import requests
from behave import given, when, then
from assertpy import assert_that
from utilities.configurations import *



@given(
    u'the user provides the email "{email}", password "{password}", returnSecureToken "{returnSecureToken}", and tenantId "{tenantId}"')
def step_impl(context, email, password, returnSecureToken, tenantId):
    # Store the input data in the context for later reference
    context.test_data = {
        "email": email,
        "password": password,
        "returnSecureToken": returnSecureToken,
        "tenantId": tenantId
    }

    # Prepare the request body
    context.request_payload = {
        "email": email,
        "password": password,
        "returnSecureToken": returnSecureToken,
        "tenantId": tenantId
    }
    config = getConfig()
    # Set up the URL and headers for the request
    context.url = config['API']['GoogleEndpoint']
    context.headers = {'Content-Type': 'application/json'}


@when(u'the user executes the API with the provided credentials')
def step_impl(context):
    # Send the POST request to the API
    context.response = requests.post(context.url, json=context.request_payload, headers=context.headers)


@then(u'the status code should be {status_code:d}')
def step_impl(context, status_code):
    # Assert that the actual status code matches the expected one
    actual_status_code = context.response.status_code
    assert_that(actual_status_code).is_equal_to(status_code)


@then(u'the error message should be "{error_message}"')
def step_impl(context, error_message):
    # Parse the response JSON
    response_json = context.response.json()

    if context.response.status_code == 200:
        # For successful responses, check if 'idToken' is present
        assert_that("idToken" in response_json).is_true()
        # Print the idToken in the console
        #print(f"idToken: {response_json['idToken']}")
    else:
        # For failure responses, check if 'error' is present and assert the error message
        assert_that("error" in response_json).is_true()
        assert_that(response_json["error"]["message"]).is_equal_to(error_message)
