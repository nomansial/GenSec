import requests
import logging
import allure
from behave import given, when, then
from assertpy import assert_that
from utilities.configurations import getConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

########################### Scenario Outline: Verify Update Customer API updates user details successfully with different data ###########################

@given(u'User sends PUT request to update customer details with "{first_name}", "{last_name}", "{job_title}", "{new_password}", and "{phone_number}"')
def step_impl(context, first_name, last_name, job_title, new_password, phone_number):
    """Send PUT request to update customer details using parameters from Examples"""
    config = getConfig()
    context.url = f"{config['API']['BaseURL']}/customers/me"

    # Fetch the API key from the configuration
    api_key = config['API']['new_customer']

    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    # Prepare request body with data from Examples
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "job_title": job_title,
        "new_password": new_password,
        "phone_number": phone_number
    }

    with allure.step("Send PUT request to Update Customer API"):
        allure.attach(str(payload), name="Request Payload", attachment_type=allure.attachment_type.JSON)
        context.response = requests.put(context.url, json=payload, headers=context.headers)
        allure.attach(str(context.response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
        allure.attach(context.response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)

    logger.info(f"Update Customer API Response: {context.response.text}")


@when(u'the user receives the response from update customer API')
def step_impl(context):
    """Ensure response is received"""
    with allure.step("Verify API response is received"):
        assert_that(context.response).is_not_none()
        allure.attach(context.response.text, name="Raw Response", attachment_type=allure.attachment_type.TEXT)
    logger.info("Response received successfully.")


@then(u'the response should contain a message "User updated successfully"')
def step_impl(context):
    """Verify success message in response"""
    with allure.step("Validate success message in response"):
        response_json = context.response.json()
        allure.attach(str(response_json), name="Parsed JSON", attachment_type=allure.attachment_type.JSON)
        assert_that(response_json.get("message")).is_equal_to("User updated successfully")
    logger.info(f"Expected: 'User updated successfully', Got: {response_json.get('message')}")


@then(u'the response should contain an error message "Invalid input"')
def step_impl(context):
    with allure.step("Validate error message in response"):
        response_json = context.response.json()
        allure.attach(str(response_json), name="Parsed JSON (Error)", attachment_type=allure.attachment_type.JSON)
        assert_that(response_json.get("message")).contains("Invalid input")
    logger.info(f"Expected: 'Invalid input', Got: {response_json.get('message')}")


@then(u'the response should contain "Invalid input:" in response body')
def step_impl(context):
    with allure.step("Check for detailed validation error"):
        response_text = context.response.text
        allure.attach(response_text, name="Full Response Text", attachment_type=allure.attachment_type.TEXT)
        assert_that(response_text).contains("Invalid input:")
    logger.info(f"Checking 'Invalid input:' in response body: {response_text}")
