import requests
import logging
from behave import given, when, then
from assertpy import assert_that
from utilities.configurations import getConfig
import time

# Set up logging to print out the response in the console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

########################### Scenario: Verify PUT request successfully updates chatbot details ###########################

@given(u'User sends PUT request to update chatbot details with chatbot_name "{chatbot_name}", chatbot_description "{chatbot_description}", and env_id "{env_id}"')
def step_impl(context, chatbot_name, chatbot_description, env_id):
    """Create chatbot, wait until status is AVAILABLE, then send PUT request to update it"""
    import time

    config = getConfig()
    base_url = config['API']['BaseURL']
    api_key = config['API']['APIKey']

    # POST request to create chatbot
    context.url = f"{base_url}/chatbots"
    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    chatbot_name = "QA Automation"
    chatbot_description = "System testing please ignore"
    env_id = "f0b53f20-5ebe-4132-cbea-68725ef2c5c8"

    payload = {
        "env_id": env_id,
        "chatbot_name": chatbot_name,
        "api_endpoint": "Jr.lzPApNRNNQR:n1Xy6WyKDPWvA@1eR5t#302OYb%lnp4ehZGwDWPoaeEDF7Nnt_hDPuK9Po2crHTiqXd-zVT9rHwiVXBEg@QvomKrjMHbJIJ8-mIswCmUY0+eYO4ZlqAg4YDUcbF@5zMaS.fozhq",
        "api_secret": "wVyB2",
        "chatbot_url": "www.t@TiGfZIdBeat:+B5XsEP4ZPRB0ZB1UI-dcArK64u@6hhfa#D8cZ+LyR:Nd0Z-glOD9q7qDSWPmJdVEx.aDTK3%#9itUKB4v7xikDUBbG~pA=qD9rVjfz6hAxgsOjZBWIkp%jyLpZj#caaQrBL",
        "chatbot_description": chatbot_description
    }

    context.response = requests.post(context.url, json=payload, headers=context.headers)
    logger.info(f"Create Chatbot API Response: {context.response.text}")
    print(f"Create Chatbot API Response: {context.response.text}")

    chatbot_id = context.response.json().get("chatbot_id")
    assert chatbot_id is not None, "chatbot_id not found in response"

    # Poll until status becomes AVAILABLE
    status_url = f"{base_url}/chatbots/{chatbot_id}"
    max_retries = 150
    wait_seconds = 10

    for attempt in range(max_retries):
        status_response = requests.get(status_url, headers={'x-api-key': api_key})
        status = status_response.json().get("status")
        logger.info(f"Attempt {attempt+1}: Chatbot status = {status}")
        print(f"Attempt {attempt+1}: Chatbot status = {status}")

        if status == "AVAILABLE":
            # Send PUT request to update chatbot details
            context.url = f"{base_url}/chatbots/{chatbot_id}"
            context.request_body = {
                "chatbot_id": chatbot_id,
                "chatbot_name": chatbot_name,
                "chatbot_description": chatbot_description,
                "env_id": env_id
            }

            context.response = requests.put(context.url, json=context.request_body, headers=context.headers)
            logger.info(f"PUT Chatbot API Response: {context.response.text}")
            print(f"PUT Chatbot API Response: {context.response.text}")
            return

        time.sleep(wait_seconds)

    assert False, f"Chatbot status did not become AVAILABLE after {max_retries} attempts"



@then(u'the response should contain the chatbot_id')
def step_impl(context):
    """Verify that the response contains the chatbot_id"""
    response_json = context.response.json()
    logger.info(f"Response contains chatbot_id: {response_json.get('chatbot_id')}")
    assert_that(response_json).contains("chatbot_id")

@then(u'the status should be In_progress')
def step_impl(context):
    """Verify that the status is 'In_progress' in the response"""
    response_json = context.response.json()
    logger.info(f"Response status: {response_json.get('status')}")
    assert_that(response_json['status']).is_equal_to("In_progress")

############################ negative scenario ################################################

@given(u'User sends PUT request to update chatbot details with chatbot_id "{chatbot_id}", chatbot_name "{chatbot_name}", chatbot_description "{chatbot_description}", and env_id "{env_id}"')
def step_impl(context, chatbot_id, chatbot_name, chatbot_description, env_id):
    """Send PUT request to update chatbot details for a given chatbot_id, chatbot_name, chatbot_description, and env_id"""
    config = getConfig()
    context.url = f"{config['API']['BaseURL']}/chatbots/{chatbot_id}"

    # Fetch the API key from the configuration
    api_key = config['API']['APIKey']  # API key fetched from the config file

    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    # Request Body
    context.request_body = {
        "chatbot_id": chatbot_id,
        "chatbot_name": chatbot_name,
        "chatbot_description": chatbot_description,
        "env_id": env_id
    }

    # Send the PUT request to update the chatbot details
    context.response = requests.put(context.url, json=context.request_body, headers=context.headers)

    # Log the PUT request response
    logger.info(f"PUT Chatbot API Response: {context.response.text}")
    print(f"PUT Chatbot API Response: {context.response.text}")  # Fallback to print in console

@then(u'the status code returned should be 400')
def step_impl(context):
    """Verify that the status code is 400 for a bad request"""
    assert_that(context.response.status_code).is_equal_to(400)

@then(u'the response should contain error variable with value Bad Request')
def step_impl(context):
    """Verify that the response contains an error variable with 'Bad Request'"""
    response_json = context.response.json()
    logger.info(f"Response contains error: {response_json.get('error')}")
    assert_that(response_json).contains("error")
    assert_that(response_json['error']).is_equal_to("Bad Request")

@then(u'the response should contain the The chatbot must be in AVAILABLE status')
def step_impl(context):
    """Verify that the response contains the message 'The chatbot must be in AVAILABLE status'"""
    response_json = context.response.json()
    logger.info(f"Response message: {response_json.get('message')}")
    assert_that(response_json['message']).contains("The chatbot must be in AVAILABLE status")

########################### SQL Injection Attempt Scenario ###########################

@given(u'User sends request with chatbot_id "{chatbot_id}", chatbot_name "{chatbot_name}", chatbot_description "{chatbot_description}", and env_id "{env_id}"')
def step_impl(context, chatbot_id, chatbot_name, chatbot_description, env_id):
    """Send PUT request with SQL injection in the chatbot details"""
    config = getConfig()
    base_url = config['API']['BaseURL']
    api_key = config['API']['APIKey']

    context.url = f"{base_url}/chatbots/{chatbot_id}"
    context.headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    context.request_body = {
        "chatbot_id": chatbot_id,
        "chatbot_name": chatbot_name,
        "chatbot_description": chatbot_description,
        "env_id": env_id
    }

    # Send the PUT request
    context.response = requests.put(context.url, json=context.request_body, headers=context.headers)

    # Log the PUT request response
    logger.info(f"PUT Chatbot API Response: {context.response.text}")
    print(f"PUT Chatbot API Response: {context.response.text}")  # Fallback to print in console


@then(u'the response should contain error variable with value "Bad Request"')
def step_impl(context):
    """Verify that the response contains the 'Bad Request' error"""
    response_json = context.response.json()
    logger.info(f"Response contains error: {response_json.get('error')}")
    assert_that(response_json).contains("error")
    assert_that(response_json['error']).is_equal_to("Bad Request")


@then(u'the response should contain invalid input message')
def step_impl(context):
    """Verify that the response contains the message 'Invalid input:'"""
    response_json = context.response.json()
    logger.info(f"Response message: {response_json.get('message')}")
    assert_that(response_json['message']).contains("Invalid input:")