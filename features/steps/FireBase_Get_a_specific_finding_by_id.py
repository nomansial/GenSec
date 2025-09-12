import requests
import logging
import re
from behave import given, when, then
from assertpy import assert_that

from utilities.authentication import get_firebase_id_token
from utilities.configurations import getConfig

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@given(u'FireBase_User sends GET request to fetch finding details for finding ID "{finding_id}"')
def step_impl(context, finding_id):
    config = getConfig()
    context.finding_id = finding_id
    context.url = f"{config['API']['FireBaseURL']}/findings/{finding_id}"
    # Get the Firebase idToken
    id_token = get_firebase_id_token()
    print(repr(id_token))
    #logger.info(f"Passing token like this: {id_token}")

    context.headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {id_token}'  # Use OAuth 2.0 Bearer token
    }
    context.response = requests.get(context.url, headers=context.headers)
    logger.info(f"Finding Details Response: {context.response.text}")
    print(f"Finding Details Response: {context.response.text}")

@when(u'FireBase_the user receives the finding details response')
def step_impl(context):
    assert_that(context.response).is_not_none()

@then(u'FireBase_the status code returned should be 200 for successful finding retrieval')
def step_impl(context):
    assert_that(context.response.status_code).is_equal_to(200)

@then(u'FireBase_the response should contain a valid "finding_id" matching "{finding_id}"')
def step_impl(context, finding_id):
    response_json = context.response.json()
    assert_that(response_json.get("finding_id")).is_equal_to(finding_id)

@then(u'FireBase_the response should contain a valid "scan_id" of length 36')
def step_impl(context):
    scan_id = context.response.json().get("scan_id")
    assert_that(scan_id).is_not_none()
    assert_that(len(scan_id)).is_equal_to(36)


@then(u'FireBase_contain a non-empty "{field}"')
def step_impl(context, field):
    value = context.response.json().get(field)
    assert_that(value).is_not_none()
    assert_that(str(value)).is_not_empty()

@then(u'FireBase_the response should contain a "creation_timestamp" in ISO 8601 format')
def step_impl(context):
    timestamp = context.response.json().get("creation_timestamp")
    assert_that(timestamp).is_not_none()
    iso8601_regex = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$"
    assert_that(re.match(iso8601_regex, timestamp)).is_not_none()

@then(u'FireBase_the response should contain non-empty lists for "data_classification" and "data_targeted"')
def step_impl(context):
    response_json = context.response.json()
    for field in ["data_classification", "data_targeted"]:
        value = response_json.get(field)
        assert_that(value).is_instance_of(list)
        assert_that(len(value)).is_greater_than(0)

# Negative Scenarios


@then(u'FireBase_the message should contain "Finding with ID {finding_id} not found."')
def step_impl(context, finding_id):
    expected_message = f"Finding with ID {finding_id} not found."
    actual_message = context.response.json().get("message")
    assert_that(actual_message).is_equal_to(expected_message)

@given(u'FireBase_the user sends GET request with finding ID')
def step_impl(context):
    config = getConfig()
    finding_id = "<script>alert('XSS');</script>"
    context.url = f"{config['API']['FireBaseURL']}/findings/{finding_id}"
    # Get the Firebase idToken
    id_token = get_firebase_id_token()
    print(repr(id_token))
    #logger.info(f"Passing token like this: {id_token}")

    context.headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {id_token}'  # Use OAuth 2.0 Bearer token
    }
    context.response = requests.get(context.url, headers=context.headers)
    logger.info(f"Finding Details Response: {context.response.text}")
    print(f"Finding Details Response: {context.response.text}")



@then(u'FireBase_the status code returned should be 404')
def step_impl(context):
    assert_that(context.response.status_code).is_equal_to(404)

@then(u'FireBase_the message should contain "The current request is not defined by this API."')
def step_impl(context):
    response_json = context.response.json()
    assert_that(response_json.get("message")).contains("The current request is not defined by this API.")


