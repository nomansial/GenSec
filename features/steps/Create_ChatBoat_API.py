import requests
import logging
from behave import given, when, then
from assertpy import assert_that
from utilities.configurations import getConfig

# Set up logging to print out the response in the console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

########################### Scenario: Verify Create Chatbot API creates a chatbot successfully ###########################

@given(u'User sends POST request to create a chatbot with valid details')
def step_impl(context):
    """Send POST request to create a chatbot with valid details"""
    config = getConfig()
    context.url = f"{config['API']['BaseURL']}/chatbots"

    # Fetch the API key from the configuration
    api_key = config['API']['APIKey']  # API key fetched from the config file

    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    # Prepare the request body to create the chatbot
    payload = {
        "env_id": "f0b53f20-5ebe-4132-cbea-68725ef2c5c8",
        "chatbot_name": "QA Automation",
        "api_endpoint": "Jr.lzPApNRNNQR:n1Xy6WyKDPWvA@1eR5t#302OYb%lnp4ehZGwDWPoaeEDF7Nnt_hDPuK9Po2crHTiqXd-zVT9rHwiVXBEg@QvomKrjMHbJIJ8-mIswCmUY0+eYO4ZlqAg4YDUcbF@5zMaS.fozhq",
        "api_secret": "wVyB2",
        "chatbot_url": "www.t@TiGfZIdBeat:+B5XsEP4ZPRB0ZB1UI-dcArK64u@6hhfa#D8cZ+LyR:Nd0Z-glOD9q7qDSWPmJdVEx.aDTK3%#9itUKB4v7xikDUBbG~pA=qD9rVjfz6hAxgsOjZBWIkp%jyLpZj#caaQrBL",
        "chatbot_description": "System testing please ignore"
    }

    # Send the POST request to create the chatbot
    context.response = requests.post(context.url, json=payload, headers=context.headers)

    # Log the Create Chatbot API response
    logger.info(f"Create Chatbot API Response: {context.response.text}")
    print(f"Create Chatbot API Response: {context.response.text}")  # Fallback to print in console


@when(u'response is received')
def step_impl(context):
    """Ensure the response is successfully received"""
    assert_that(context.response).is_not_none()
    logger.info("Response received successfully.")


@then(u'the status code returned should be 200 for the created chatbot')
def step_impl(context):
    """Verify that the status code for the create request is 200"""
    logger.info(f"Expected Status Code: 200, Got: {context.response.status_code}")
    assert_that(context.response.status_code).is_equal_to(200)


@then(u'the response should contain a "chatbot_id"')
def step_impl(context):
    """Verify that the response contains 'chatbot_id'"""
    response_json = context.response.json()
    logger.info(f"Response contains chatbot_id: {response_json.get('chatbot_id')}")
    assert_that(response_json).contains("chatbot_id")


########################### Scenario: Verify Create Chatbot API when the chatbot name is invalid ###########################

@given(u'User sends POST request to create a chatbot with an invalid chatbot name "{chatbot_name}"')
def step_impl(context, chatbot_name):
    """Send POST request to create a chatbot with an invalid chatbot name"""
    config = getConfig()
    context.url = f"{config['API']['BaseURL']}/chatbots"

    # Fetch the API key from the configuration
    api_key = config['API']['APIKey']  # API key fetched from the config file

    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    # Prepare the request body with an invalid chatbot name (using None to represent null)
    payload = {
        "env_id": "f0b53f20-5ebe-4132-cbea-68725ef2c5c8",
        "chatbot_name": None if chatbot_name == "None" else chatbot_name,  # Use None for null
        "api_endpoint": "Jr.lzPApNRNNQR:n1Xy6WyKDPWvA@1eR5t#302OYb%lnp4ehZGwDWPoaeEDF7Nnt_hDPuK9Po2crHTiqXd-zVT9rHwiVXBEg@QvomKrjMHbJIJ8-mIswCmUY0+eYO4ZlqAg4YDUcbF@5zMaS.fozhq",
        "api_secret": "wVyB2",
        "chatbot_url": "www.t@TiGfZIdBeat:+B5XsEP4ZPRB0ZB1UI-dcArK64u@6hhfa#D8cZ+LyR:Nd0Z-glOD9q7qDSWPmJdVEx.aDTK3%#9itUKB4v7xikDUBbG~pA=qD9rVjfz6hAxgsOjZBWIkp%jyLpZj#caaQrBL",
        "chatbot_description": "System testing please ignore"
    }

    # Send the POST request to create the chatbot with invalid name (null)
    context.response = requests.post(context.url, json=payload, headers=context.headers)

    # Log the Create Chatbot API response
    logger.info(f"Create Chatbot API Response (Invalid Name): {context.response.text}")
    print(f"Create Chatbot API Response (Invalid Name): {context.response.text}")  # Fallback to print in console


@then(u'the response should contain an error message "Bad Request"')
def step_impl(context):
    """Verify that the response contains 'Bad Request' error message"""
    response_json = context.response.json()
    logger.info(f"Expected error message: 'Bad Request', Got: {response_json.get('error')}")
    assert_that(response_json.get("error")).is_equal_to("Bad Request")


@then(u'the message should contain "Invalid input:"')
def step_impl(context):
    """Verify that the error message contains 'Invalid input:'"""
    response_json = context.response.json()
    logger.info(f"Expected error message: 'Invalid input:', Got: {response_json.get('message')}")
    assert_that(response_json.get("message")).contains("Invalid input:")


########################### Scenario: Verify Create Chatbot API when required fields are missing ###########################

@given(u'User sends POST request to create a chatbot with missing required fields "{field}"')
def step_impl(context, field):
    """Send POST request to create a chatbot with missing required fields"""
    config = getConfig()
    context.url = f"{config['API']['BaseURL']}/chatbots"

    # Fetch the API key from the configuration
    api_key = config['API']['APIKey']  # API key fetched from the config file

    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    # Prepare the request body with the missing field
    payload = {
        "env_id": "f0b53f20-5ebe-4132-cbea-68725ef2c5c8" if field != "env_id" else None,
        "chatbot_name": "QA Automation" if field != "chatbot_name" else None,
        "api_endpoint": "Jr.lzPApNRNNQR:n1Xy6WyKDPWvA@1eR5t#302OYb%lnp4ehZGwDWPoaeEDF7Nnt_hDPuK9Po2crHTiqXd-zVT9rHwiVXBEg@QvomKrjMHbJIJ8-mIswCmUY0+eYO4ZlqAg4YDUcbF@5zMaS.fozhq" if field != "api_endpoint" else None,
        "api_secret": "wVyB2" if field != "api_secret" else None,
        "chatbot_url": "www.t@TiGfZIdBeat:+B5XsEP4ZPRB0ZB1UI-dcArK64u@6hhfa#D8cZ+LyR:Nd0Z-glOD9q7qDSWPmJdVEx.aDTK3%#9itUKB4v7xikDUBbG~pA=qD9rVjfz6hAxgsOjZBWIkp%jyLpZj#caaQrBL" if field != "chatbot_url" else None,
        "chatbot_description": "System testing please ignore" if field != "chatbot_description" else None
    }

    # Send the POST request to create the chatbot with missing field
    context.response = requests.post(context.url, json=payload, headers=context.headers)

    # Log the Create Chatbot API response
    logger.info(f"Create Chatbot API Response (Missing Field {field}): {context.response.text}")
    print(f"Create Chatbot API Response (Missing Field {field}): {context.response.text}")  # Fallback to print in console


@then(u'the status code should be 400 for bad request error')
def step_impl(context):
    """Verify that the status code for the error is 400"""
    logger.info(f"Expected Status Code: 400, Got: {context.response.status_code}")
    assert_that(context.response.status_code).is_equal_to(400)


