import requests
import logging
import re
from behave import given, when, then
from assertpy import assert_that

from utilities.authentication import get_firebase_id_token
from utilities.configurations import getConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@given(u'FireBase_User sends GET request to fetch scans for chatbot ID "{chatbot_id}"')
def step_impl(context, chatbot_id):
    """Send GET request to fetch scans for a given chatbot ID"""
    config = getConfig()
    context.chatbot_id = chatbot_id
    context.url = f"{config['API']['FireBaseURL']}/scans?chatbot_id={chatbot_id}"

    # Get the Firebase idToken
    id_token = get_firebase_id_token()
    print(repr(id_token))
    #logger.info(f"Passing token like this: {id_token}")

    context.headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {id_token}'  # Use OAuth 2.0 Bearer token
    }

    context.response = requests.get(context.url, headers=context.headers)
    logger.info(f"Scans Response: {context.response.text}")
    print(f"Scans Response: {context.response.text}")

@when(u'FireBase_the user receives the scans response')
def step_impl(context):
    """Ensure the scans response is received"""
    assert_that(context.response).is_not_none()

@then(u'FireBase_the status code returned should be 200 for successful scans retrieval')
def step_impl(context):
    """Verify status code is 200"""
    assert_that(context.response.status_code).is_equal_to(200)

@then(u'FireBase_the response should contain a list of scans')
def step_impl(context):
    """Check that scans list is present and not empty"""
    response_json = context.response.json()
    scans = response_json.get("scans")
    assert_that(scans).is_not_none()
    assert_that(scans).is_instance_of(list)
    assert_that(len(scans)).is_greater_than(0)
    context.scans = scans

@then(u'FireBase_each scan should contain a valid "scan_id" of length 36')
def step_impl(context):
    """Validate scan_id format for each scan"""
    for scan in context.scans:
        scan_id = scan.get("scan_id")
        assert_that(scan_id).is_not_none()
        assert_that(len(scan_id)).is_equal_to(36)

@then(u'FireBase_each scan should contain a "creation_timestamp" in ISO 8601 format')
def step_impl(context):
    """Validate creation_timestamp format for each scan"""
    iso8601_regex = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z$"
    for scan in context.scans:
        timestamp = scan.get("creation_timestamp")
        assert_that(timestamp).is_not_none()
        # Convert timestamp to ISO 8601 format if needed
        converted = timestamp.replace(" ", "T").replace("+00:00", "Z")
        assert_that(re.match(iso8601_regex, converted)).is_not_none()

@then(u'FireBase_each scan should have a "status" equal to "REPORT_GENERATED"')
def step_impl(context):
    """Validate status field for each scan"""
    for scan in context.scans:
        status = scan.get("status")
        assert_that(status).is_not_none()


@then(u'FireBase_the response should contain an empty list of scans')
def step_impl(context):
    """Validate that the scans list is empty"""
    response_json = context.response.json()
    scans = response_json.get("scans")
    assert_that(scans).is_instance_of(list)
    assert_that(len(scans)).is_equal_to(0)






