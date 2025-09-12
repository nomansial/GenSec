import requests
from behave import given, when, then
from assertpy import assert_that
from utilities.configurations import getConfig

@given(u'the user sends a GET request to retrieve the environments using APIKey')
def step_impl(context):
    config = getConfig()
    url = f"{config['API']['BaseURL']}/environments"
    api_key = config['API'].get('APIKey', '')
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }
    context.response_api_key = requests.get(url, headers=headers)

@given(u'the user sends a GET request to retrieve the environments using APIKey2')
def step_impl(context):
    config = getConfig()
    url = f"{config['API']['BaseURL']}/environments"
    api_key2 = config['API'].get('APIKey2', '')
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key2
    }
    context.response_api_key2 = requests.get(url, headers=headers)

@when(u'the user receives the response')
def step_impl(context):
    pass

@when(u'Firebase_the user receives the response')
def step_impl(context):
    pass


@then(u'the status code returned should be 200')
def step_impl(context):
    response = getattr(context, 'response_api_key2', getattr(context, 'response_api_key', None))
    assert_that(response).is_not_none()
    assert_that(response.status_code).is_equal_to(200)

@then(u'each environment should have a non-null "env_id" and "name"')
def step_impl(context):
    try:
        response_json = context.response_api_key.json()
        environments = response_json.get("environments", [])
        for env in environments:
            assert_that(env.get("env_id")).is_not_none().is_not_empty()
            assert_that(env.get("name")).is_not_none().is_not_empty()
    except ValueError:
        assert False, "Failed to parse response JSON"

@then(u'the user stores the list of environments returned')
def step_impl(context):
    try:
        response_json = context.response_api_key.json()
        context.envs_api_key = response_json.get("environments", [])
    except ValueError:
        assert False, "Failed to parse response JSON"

@then(u'the environments returned should not match those from APIKey')
def step_impl(context):
    try:
        response_json = context.response_api_key2.json()
        envs_api_key2 = response_json.get("environments", [])
        assert_that(envs_api_key2).is_not_equal_to(context.envs_api_key)
    except ValueError:
        assert False, "Failed to parse response JSON"

@given(u'the user sends a GET request to retrieve the environments using an invalid API key')
def step_impl(context):
    config = getConfig()
    url = f"{config['API']['BaseURL']}/environments"
    invalid_api_key = config['API'].get('Invalid_Key', '')  # Replace with an actual invalid key if needed
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': invalid_api_key
    }
    context.response_invalid_api_key = requests.get(url, headers=headers)

@then(u'status code be 400')
def step_impl(context):
    response = context.response_invalid_api_key
    assert_that(response).is_not_none()
    assert_that(response.status_code).is_equal_to(400)

@then(u'the response should contain code 400')
def step_impl(context):
    response_json = context.response_invalid_api_key.json()
    assert_that(response_json.get('code')).is_equal_to(400)

@then(u'the response should contain the message "INVALID_ARGUMENT:"')
def step_impl(context):
    response_json = context.response_invalid_api_key.json()
    assert_that(response_json.get('message')).contains("INVALID_ARGUMENT:")


@given(u'the user sends a GET request with a malicious payload')
def step_impl(context):
    config = getConfig()
    url = f"{config['API']['BaseURL']}/environments"
    malicious_payload = "' OR 1=1 --"
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': config['API'].get('APIKey', '')
    }
    context.response_sql_injection = requests.get(url + f"?query={malicious_payload}", headers=headers)

@given(u'the user sends a GET request with a XSS attempt')
def step_impl(context):
    config = getConfig()
    url = f"{config['API']['BaseURL']}/environments"
    malicious_payload = "<script>alert('XSS')</script>"
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': config['API'].get('APIKey', '')
    }
    context.response_sql_injection = requests.get(url + f"?name={malicious_payload}", headers=headers)


@then(u'the response should contain the message Invalid input')
def step_impl(context):
    response_json = context.response_sql_injection.json()
    assert_that(response_json.get('message')).contains("Invalid input:")
