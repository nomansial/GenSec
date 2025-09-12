import requests
import logging
from behave import given, when, then
from assertpy import assert_that

from utilities.authentication import get_firebase_id_token
from utilities.configurations import getConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

########################### Scenario Outline: Verify Update Customer API updates user details successfully with different data ###########################

@given(u'FireBase_User sends PUT request to update customer details with "{first_name}", "{last_name}", "{job_title}", "{new_password}", and "{phone_number}"')
def step_impl(context, first_name, last_name, job_title, new_password, phone_number):
    """Send PUT request to update customer details using parameters from Examples"""
    config = getConfig()
    context.url = f"{config['API']['FireBaseURL']}/customers/me"

    # Get the Firebase idToken
    id_token = get_firebase_id_token()
    print(repr(id_token))
    #logger.info(f"Passing token like this: {id_token}")

    context.headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {id_token}'  # Use OAuth 2.0 Bearer token
    }

    # Prepare request body with data from Examples
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "job_title": job_title,
        "new_password": new_password,
        "phone_number": phone_number
    }

    # Send PUT request with JSON body
    context.response = requests.put(context.url, json=payload, headers=context.headers)

    # Log response
    logger.info(f"Update Customer API Response: {context.response.text}")
    print(f"Update Customer API Response: {context.response.text}")  # fallback for console


@when(u'FireBase_the user receives the response from update customer API')
def step_impl(context):
    """Ensure response is received"""
    assert_that(context.response).is_not_none()
    logger.info("Response received successfully.")


@then(u'FireBase_the response should contain a message "User updated successfully"')
def step_impl(context):
    """Verify success message in response"""
    response_json = context.response.json()
    logger.info(f"Expected message: 'User updated successfully', Got: {response_json.get('message')}")
    assert_that(response_json.get("message")).is_equal_to("User updated successfully")


@then(u'FireBase_the response should contain an error message "Invalid input"')
def step_impl(context):
    response_json = context.response.json()
    logger.info(f"Expected error message: 'Invalid input', Got: {response_json.get('message')}")
    assert_that(response_json.get("message")).contains("Invalid input")

@then(u'FireBase_the response should contain "Invalid input:" in response body')
def step_impl(context):
    response_text = context.response.text
    logger.info(f"Checking for 'Invalid input:' in response body: {response_text}")
    assert_that(response_text).contains("Invalid input:")


