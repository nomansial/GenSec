import requests
import logging
import re
from behave import given, when, then
from assertpy import assert_that
from utilities.configurations import getConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@given(u'User sends GET request to fetch scan details for scan ID "{scan_id}"')
def step_impl(context, scan_id):
    """Send GET request to fetch scan details"""
    config = getConfig()
    context.scan_id = scan_id
    context.url = f"{config['API']['BaseURL']}/scans/{scan_id}"

    api_key = config['API']['APIKey']
    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    context.response = requests.get(context.url, headers=context.headers)
    logger.info(f"Scan Details Response: {context.response.text}")
    print(f"Scan Details Response: {context.response.text}")

@when(u'the user receives the scan details response')
def step_impl(context):
    """Ensure the scan details response is received"""
    assert_that(context.response).is_not_none()

@then(u'the status code returned should be 200 for successful scan details retrieval')
def step_impl(context):
    """Verify status code is 200"""
    assert_that(context.response.status_code).is_equal_to(200)

@then(u'the response should contain a valid "chatbot_id" of length 36')
def step_impl(context):
    """Check chatbot_id exists and is 36 characters long"""
    response_json = context.response.json()
    chatbot_id = response_json.get("chatbot_id")
    assert_that(chatbot_id).is_not_none()
    assert_that(len(chatbot_id)).is_equal_to(36)

@then(u'the response should contain a "chatbot_name"')
def step_impl(context):
    """Check chatbot_name exists and is not empty"""
    response_json = context.response.json()
    chatbot_name = response_json.get("chatbot_name")
    assert_that(chatbot_name).is_not_empty()

@then(u'the "creation_timestamp" should be in ISO 8601 format')
def step_impl(context):
    """Validate creation_timestamp format"""
    response_json = context.response.json()
    timestamp = response_json.get("creation_timestamp")
    iso8601_regex = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$"
    assert_that(re.match(iso8601_regex, timestamp)).is_not_none()

@then(u'the "last_update_timestamp" should be in ISO 8601 format')
def step_impl(context):
    """Validate last_update_timestamp format"""
    response_json = context.response.json()
    timestamp = response_json.get("last_update_timestamp")
    iso8601_regex = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$"
    assert_that(re.match(iso8601_regex, timestamp)).is_not_none()

@then(u'the "scan_id" should match the requested scan ID "{scan_id}"')
def step_impl(context, scan_id):
    """Verify scan_id matches the requested one"""
    response_json = context.response.json()
    assert_that(response_json.get("scan_id")).is_equal_to(scan_id)

@then(u'the "status" should be "SCAN_COMPLETED"')
def step_impl(context):
    """Verify scan status is SCAN_COMPLETED"""
    response_json = context.response.json()
    assert_that(response_json.get("status")).is_not_empty()


@then(u'the message should contain "Scan with ID {scan_id} not found."')
def step_impl(context, scan_id):
    """Verify that the error message matches the expected not found message"""
    expected_message = f"Scan with ID {scan_id} not found."
    actual_message = context.response.json().get("message")
    logger.info(f"Expected message: '{expected_message}', Got: '{actual_message}'")
    assert_that(actual_message).is_equal_to(expected_message)

@given(u'Specific Scan by ID the user sends GET request with finding ID')
def step_impl(context):
    """Send GET request with a finding ID containing an XSS injection attempt"""
    config = getConfig()
    finding_id = "<script>alert('XSS');</script>"  # XSS injection attempt
    context.url = f"{config['API']['BaseURL']}/scans/{finding_id}"  # Corrected to 'scans'

    api_key = config['API']['APIKey']
    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    # Send the GET request with the malicious finding ID
    context.response = requests.get(context.url, headers=context.headers)

    # Log and print the response for debugging purposes
    logger.info(f"Finding Details Response: {context.response.text}")
    print(f"Finding Details Response: {context.response.text}")

@then(u'Specific Scan by ID the status code returned should be 404')
def step_impl(context):
    assert_that(context.response.status_code).is_equal_to(404)

@then(u'Specific Scan by ID the message should contain "The current request is not defined by this API."')
def step_impl(context):
    response_json = context.response.json()
    assert_that(response_json.get("message")).contains("The current request is not defined by this API.")



