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

@given(u'FireBase_User sends GET request to fetch findings for scan ID "{scan_id}"')
def step_impl(context, scan_id):
    config = getConfig()
    context.scan_id = scan_id
    context.url = f"{config['API']['FireBaseURL']}/findings?scan_id={scan_id}"
    # Get the Firebase idToken
    id_token = get_firebase_id_token()
    print(repr(id_token))
    #logger.info(f"Passing token like this: {id_token}")

    context.headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {id_token}'  # Use OAuth 2.0 Bearer token
    }
    context.response = requests.get(context.url, headers=context.headers)
    logger.info(f"Findings Response: {context.response.text}")
    print(f"Findings Response: {context.response.text}")

@when(u'FireBase_the user receives the findings response')
def step_impl(context):
    assert_that(context.response).is_not_none()

@then(u'FireBase_the status code returned should be 200 for successful findings retrieval')
def step_impl(context):
    assert_that(context.response.status_code).is_equal_to(200)

@then(u'FireBase_the response contain a valid "chatbot_id" of length 36')
def step_impl(context):
    chatbot_id = context.response.json().get("chatbot_id")
    assert_that(chatbot_id).is_not_none()
    assert_that(len(chatbot_id)).is_equal_to(36)

@then(u'FireBase_the response should contain a non-empty "chatbot_name"')
def step_impl(context):
    chatbot_name = context.response.json().get("chatbot_name")
    assert_that(chatbot_name).is_not_none()
    assert_that(str(chatbot_name)).is_not_empty()

@then(u'FireBase_the "scan_id" in response should match "{scan_id}"')
def step_impl(context, scan_id):
    actual_scan_id = context.response.json().get("scan_id")
    assert_that(actual_scan_id).is_equal_to(scan_id)

@then(u'FireBase_the response should contain a non-empty list of findings')
def step_impl(context):
    findings = context.response.json().get("findings")
    assert_that(findings).is_instance_of(list)
    assert_that(len(findings)).is_greater_than(0)
    context.findings = findings

@then(u'FireBase_each finding should include the following fields:')
def step_impl(context):
    """Validate required fields in each finding"""
    required_fields = [row.cells[0] for row in context.table]  # Use cells[0] for single-column table
    for finding in context.findings:
        for field in required_fields:
            value = finding.get(field)
            assert_that(value).is_not_none()
            assert_that(str(value)).is_not_empty()


@then(u'FireBase_each finding with a "creation_timestamp" should be in ISO 8601 format')
def step_impl(context):
    iso8601_regex = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$"
    for finding in context.findings:
        timestamp = finding.get("creation_timestamp")
        if timestamp:
            assert_that(re.match(iso8601_regex, timestamp)).is_not_none()


@then(u'FireBase_the response should contain null "chatbot_id" and "chatbot_name"')
def step_impl(context):
    response_json = context.response.json()
    assert_that(response_json.get("chatbot_id")).is_none()
    assert_that(response_json.get("chatbot_name")).is_none()

@then(u'FireBase_the response should contain an empty list of findings')
def step_impl(context):
    findings = context.response.json().get("findings")
    assert_that(findings).is_instance_of(list)
    assert_that(len(findings)).is_equal_to(0)




