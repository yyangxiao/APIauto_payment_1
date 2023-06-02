import requests

# url = "https://api.stripe.com/v1/payment_intents/pi_3N7yRMIZwcIFVLGr2xsld2QG/confirm"
#
# payload = 'return_url=https%3A%2F%2Fclient.t2.moego.pet%2Fpayment%2Fonline%2F57576e549dfd403d928784d26703528f&payment_method_data%5Btype%5D=card&payment_method_data%5Bcard%5D%5Bnumber%5D=4000%2B0025%2B0000%2B3155&payment_method_data%5Bcard%5D%5Bcvc%5D=111&payment_method_data%5Bcard%5D%5Bexp_year%5D=24&payment_method_data%5Bcard%5D%5Bexp_month%5D=11&payment_method_data%5Bbilling_details%5D%5Baddress%5D%5Bcountry%5D=TW&payment_method_data%5Bpayment_user_agent%5D=stripe.js%2F4fa8c9826f%3B%2Bstripe-js-v3%2F4fa8c9826f%3B%2Bpayment-element&payment_method_data%5Btime_on_page%5D=408022&payment_method_data%5Bguid%5D=0036cd05-b169-497d-a782-ae3d76670a5e2158b1&payment_method_data%5Bmuid%5D=ec7de802-e823-41ba-bdb5-b9058ecb6b3195c225&payment_method_data%5Bsid%5D=59f267cb-a24b-4007-99bb-75d807de7beec267b2&expected_payment_method_type=card&use_stripe_sdk=true&key=pk_test_iE6oFDNcmBgkuWlPFWuShPfo&client_secret=pi_3N7yRMIZwcIFVLGr2xsld2QG_secret_zebX3CDSfpSVyI6ovYEZPrELo'
# headers = {'content-type': 'application/x-www-form-urlencoded',}
#
# response = requests.request("POST", url, headers=headers, data=payload)
#
# print(response.text)

def stripe_payment_intents(paymentIntentId,payload):
    url="https://api.stripe.com/v1/payment_intents/"+paymentIntentId+"/confirm"
    header = {'content-type': 'application/x-www-form-urlencoded'}
    response=requests.post(url=url,data=payload,headers=header)
    return response

