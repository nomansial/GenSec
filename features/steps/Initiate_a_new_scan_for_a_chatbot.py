import requests
import logging
from behave import given, when, then
from assertpy import assert_that
from utilities.configurations import getConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@given(u'User sends POST request to initiate a scan with chatbot "{target_chatbot}" and environment "{target_env}"')
def step_impl(context, target_chatbot, target_env):
    """Send POST request to initiate a scan with valid chatbot and environment IDs"""
    config = getConfig()
    context.url = f"{config['API']['BaseURL']}/scans"

    # Fetch the API key from the configuration
    api_key = config['API']['APIKey']

    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    # Prepare the request body
    payload = {
        "target_chatbot": target_chatbot,
        "target_env": target_env
    }

    # Send the POST request
    context.response = requests.post(context.url, json=payload, headers=context.headers)

    # Log the response
    logger.info(f"Scan Initiation Response: {context.response.text}")
    print(f"Scan Initiation Response: {context.response.text}")

@when(u'the user receives the scan initiation response')
def step_impl(context):
    """Ensure the scan initiation response is received"""
    assert_that(context.response).is_not_none()
    logger.info("Scan initiation response received.")

@then(u'the status code returned should be 200 for successful scan initiation')
def step_impl(context):
    """Verify that the status code is 200"""
    logger.info(f"Expected Status Code: 200, Got: {context.response.status_code}")
    assert_that(context.response.status_code).is_equal_to(200)

@then(u'the response should contain a "scan_id"')
def step_impl(context):
    """Verify that the response contains 'scan_id'"""
    response_json = context.response.json()
    logger.info(f"Response contains scan_id: {response_json.get('scan_id')}")
    assert_that(response_json).contains("scan_id")

@then(u'the response status should be "SCAN_REQUESTED"')
def step_impl(context):
    """Verify that the response status is 'SCAN_REQUESTED'"""
    response_json = context.response.json()
    logger.info(f"Expected status: 'SCAN_REQUESTED', Got: {response_json.get('status')}")
    assert_that(response_json.get("status")).is_equal_to("SCAN_REQUESTED")


@then(u'the status code returned should be 404 for not found error')
def step_impl(context):
    """Verify that the status code is 404"""
    logger.info(f"Expected Status Code: 404, Got: {context.response.status_code}")
    assert_that(context.response.status_code).is_equal_to(404)



@then(u'the message should contain "Provided Chatbot {target_chatbot} not found in Environment {target_env}.Both chatbot and environment should exist and chatbot should be assigned to the environment."')
def step_impl(context, target_chatbot, target_env):
    """Verify that the message contains the expected error detail"""
    expected_message = (
        f"Provided Chatbot {target_chatbot} not found in Environment {target_env}.Both chatbot and environment should exist and chatbot should be assigned to the environment."
    )
    response_json = context.response.json()
    actual_message = response_json.get("message")
    logger.info(f"Expected message: '{expected_message}', Got: '{actual_message}'")
    assert_that(actual_message).is_equal_to(expected_message)

############################ Invalid Scenario ###################
@then(u'the status code returned should be 400 for bad request error')
def step_impl(context):
    """Verify that the status code is 400"""
    logger.info(f"Expected Status Code: 400, Got: {context.response.status_code}")
    assert_that(context.response.status_code).is_equal_to(400)



