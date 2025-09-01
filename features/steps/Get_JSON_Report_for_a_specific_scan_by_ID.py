import requests
import logging
import re
from behave import given, when, then
from assertpy import assert_that
from utilities.configurations import getConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@given(u'User sends GET request to fetch JSON report for scan ID "{scan_id}"')
def step_impl(context, scan_id):
    """Send GET request to fetch JSON report for a given scan ID"""
    config = getConfig()
    context.scan_id = scan_id
    context.url = f"{config['API']['BaseURL']}/scans/{scan_id}/json"

    api_key = config['API']['APIKey']
    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    context.response = requests.get(context.url, headers=context.headers)
    logger.info(f"JSON Report Response: {context.response.text}")
    print(f"JSON Report Response: {context.response.text}")

@when(u'the user receives the JSON report response')
def step_impl(context):
    """Ensure the JSON report response is received"""
    assert_that(context.response).is_not_none()

@then(u'the status code returned should be 200 for successful report retrieval')
def step_impl(context):
    """Verify status code is 200"""
    assert_that(context.response.status_code).is_equal_to(200)

@then(u'chatboatname should contain a "chatbot_name"')
def step_impl(context):
    """Check chatbot_name exists and is not empty"""
    report = context.response.json().get("report_json")
    assert_that(report).is_not_none()
    chatbot_name = report.get("chatbot_name")
    assert_that(chatbot_name).is_not_none()
    assert_that(str(chatbot_name)).is_not_empty()

@then(u'the response should contain a valid "scan_id" matching "{scan_id}"')
def step_impl(context, scan_id):
    """Verify scan_id matches the requested one"""
    report = context.response.json().get("report_json")
    assert_that(report).is_not_none()
    assert_that(report.get("scan_id")).is_equal_to(scan_id)

@then(u'the response should contain a "start_timestamp" in ISO 8601 format')
def step_impl(context):
    """Validate start_timestamp format"""
    report = context.response.json().get("report_json")
    timestamp = report.get("start_timestamp")
    assert_that(timestamp).is_not_none()
    iso8601_regex = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$"
    assert_that(re.match(iso8601_regex, timestamp)).is_not_none()

@then(u'the response should contain an "end_timestamp" in ISO 8601 format')
def step_impl(context):
    """Validate end_timestamp format"""
    report = context.response.json().get("report_json")
    timestamp = report.get("end_timestamp")
    assert_that(timestamp).is_not_none()
    iso8601_regex = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$"
    assert_that(re.match(iso8601_regex, timestamp)).is_not_none()

@then(u'the response should contain a list of findings')
def step_impl(context):
    """Check findings list exists and is not empty"""
    report = context.response.json().get("report_json")
    findings = report.get("findings")
    assert_that(findings).is_instance_of(list)
    assert_that(len(findings)).is_greater_than(0)
    context.findings = findings

@then(u'each finding should contain:')
def step_impl(context):
    """Validate required fields in each finding"""
    required_fields = [row['name'] for row in context.table]
    for finding in context.findings:
        for field in required_fields:
            value = finding.get(field)
            assert_that(value).is_not_none()
            if isinstance(value, list):
                assert_that(len(value)).is_greater_than(0)
            else:
                assert_that(str(value)).is_not_empty()

@then(u'the response should contain the error "Bad Request"')
def step_impl(context):
    """Check if the response contains the specified error message"""
    response_json = context.response.json()
    assert_that(response_json.get("error")).is_equal_to('Bad Request')

@then(u'the response should contain the error message "Invalid input:"')
def step_impl(context):
    """Check if the response contains the specified error message"""
    response_json = context.response.json()
    assert_that(response_json.get("message")).contains('Invalid input:')

@then(u'the response should contain the message "The current request is not defined by this API."')
def step_impl(context):
    """Check if the response contains the specific error message for XSS attack"""
    response_json = context.response.json()
    assert_that(response_json.get("message")).is_equal_to("The current request is not defined by this API.")
