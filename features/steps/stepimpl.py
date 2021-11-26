from behave import *
import requests
from assertpy import assert_that

from payLoads.payLoad import *
from utilities.resources import *

from utilities.configurations import *
config = getConfig()


@given(u'user basic information is provided')
def step_impl(context):
    context.url = config['API']['endpoint']
    context.headers = {'Content-Type': 'application/json'}


@when(u'user executed API with {amount}')
def step_impl(context, amount):
    context.registerMerchant_response = requests.post(context.url, registerMerchantPayload(amount), headers=context.headers)


@then(u'status code should be {statusCode:d}')
def step_impl(context, statusCode):
    status_code = context.registerMerchant_response.status_code
    assert_that(status_code).is_equal_to(statusCode)
