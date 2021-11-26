from utilities.configurations import *


def registerMerchantPayload(amount):
    body = {
        "@version": "2.0",
        "Currency": "AED",
        "OrderName": "Test Java",
        "OrderInfo": "OrderInfo",
        "ReturnPath": "http://demo-ipg.comtrust.ae/test",
        "OrderID": "TEST{Y}{m}{d}",
        "ExtraData": {
            "HelloWorld": "I am in ExtraData"
        },
        "Channel": "Web",
        "Amount": amount,
        "TransactionHint": "CPT:N",
        "Customer": "Demo Merchant"
    }
    return body
