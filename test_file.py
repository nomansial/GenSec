import requests
from assertpy import assert_that

from payLoads.payLoad import *
from utilities.resources import *

from utilities.configurations import *

config = getConfig()

url = config['API']['endpoint']
headers = {'Content-Type': 'application/json'}

registerMerchant_response = requests.post(url, registerMerchantPayload(), headers=headers)

status_code = registerMerchant_response.status_code

assert_that(status_code).is_equal_to(200)
