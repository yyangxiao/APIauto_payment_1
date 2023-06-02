import requests
from data import *


def business_account_login(email,pwd):
    url=host+'business/account/login'
    payload={"email":email,"password":pwd}
    header={"content-type":"application/json"}
    response=requests.post(url=url,json=payload,headers=header)
    return response

def business_account_info_v2(header):
    url=host+'business/account/info-v2'
    response=requests.get(url=url,headers=header)
    return response

def customer_smartList(header):
    url=host+"customer/smart-list"
    payload=smartListParam
    response=requests.post(url=url,headers=header,json=payload)
    # print(response.text)
    return response

def grooming_services(customerId,petId,header):
    url=host+'grooming/services'
    payload={"customerId":customerId,"petId":petId}
    response=requests.get(url=url,params=payload,headers=header)
    # print(response.text)
    return response

def business_staff_list(header):
    url=host+'business/staff/list'
    response=requests.post(url=url,json={},headers=header)
    return response

def grooming_appointment_POST(payload,header):
    url=host+"grooming/appointment"
    response=requests.post(url=url,json=payload,headers=header)
    return response

def grooming_appointment_detail_pup(header,groomingId):
    url=host+"grooming/appointment/detail/pup"
    payload={"id":groomingId}
    response=requests.get(url=url,params=payload,headers=header)
    return response

def grooming_invoice_order_detail(header,orderId):
    url=host+"grooming/invoice/order/detail"
    payload={"orderId":orderId}
    response=requests.get(url=url,params=payload,headers=header)
    return response

def business_setting(header):
    url=host+"business/setting"
    response = requests.get(url=url, headers=header)
    return response

def business_info(header,payload):
    url=host+'business/info'
    response=requests.put(url=url,json=payload,headers=header)
    return response

def payment_setting_info(header):
    '''

    :param header:
    :return: {
    "businessId":100741,
    "processingFeePayBy":1, 1：by client ;2: by business
    "processingFeeCalMethod":1,
    "processingFeeSignature":"https://moegonew.s3-us-west-2.amazonaws.com/Public/Uploads/1681884811244f62fad5ce4e3c8ef582fc4c23884a.processing_fee_signature_100741_1681884811329",
    "signatureTime":1681884813,
    "onlineFeeRate":3.40,
    "onlineFeeCents":30,
    "readerFeeRate":2.95,
    "readerFeeCents":41,
    "customizedFeeName":"wavvenience fee55666",
    "skipTipping":0,
    "cardAuthEnable":1,
    "autoCancelFeeByClient":0,
    "closeCustomRate":0,
    "allowCustomRate":1,
    "customTipping":"{\"headerText\":\"Have a pawfect Easter day!aaaaaansjsndjdk\",\"theme\":\"Classic\",\"colorConfig\":{\"presetColor\":\"#AF52DE\",\"isSelectCustom\":false,\"customColor\":\"#000000\",\"customType\":0}}","createTime":"2022-10-10T07:46:00.000+00:00","updateTime":"2023-05-05T08:20:52.000+00:00"}
    '''
    url=host+"payment/setting/info"
    response=requests.get(url=url,headers=header)
    return response

def payment_setting_info_put(header,payload):
    url=host+'payment/setting/info'
    response=requests.put(url=url,json=payload,headers=header)
    return response

def payment_payment_processingFee(header,amount,stripePaymentMethod):
    url=host+'payment/payment/processingFee'
    payload={"amount":amount,"stripePaymentMethod":stripePaymentMethod}
    response=requests.get(url=url,params=payload,headers=header)
    return  response

def payment_payment_createAndConfirm(header,payload,tokenBusinessId):
    url=host+"payment/payment/createAndConfirm"
    param={"tokenBusinessId":tokenBusinessId}
    response=requests.post(url=url,json=payload,params=param,headers=header)
    return response

def grooming_invoice_order_detail(header,orderId):
    url=host+'grooming/invoice/order/detail'
    para={"orderId":orderId}
    response=requests.get(url=url,params=para,headers=header)
    return response

def grooming_invoice_client_url(header,invoiceId,requiredProcessingFee):
    url=host+'grooming/invoice/client/url'
    para={"invoiceId":invoiceId,"requiredProcessingFee":requiredProcessingFee}
    response=requests.get(url=url,params=para,headers=header)
    return response

def grooming_appointment_cancel(header,groomingId,noShow,cancelReason):
    url=host+'grooming/appointment/cancel'
    payload={"id":groomingId,"noShow":noShow,"cancelReason":cancelReason}
    response = requests.put(url=url, json=payload, headers=header)
    return response

def grooming_invoice_noshow(header,amount,groomingId):
    url = host + "grooming/invoice/noshow"
    payload = {"amount": amount,"groomingId":groomingId}
    response = requests.post(url=url, json=payload, headers=header)
    return response

def payment_cof_code(header,customerId):
    url=host+'payment/cof/code'
    para={"customerId":customerId}
    response=requests.put(url=url,params=para,headers=header)
    return response

def payment_stripe_getConnectedInfo(header):
    url=host+'payment/stripe/getConnectedInfo'
    response=requests.get(url=url,headers=header).json()
    accBalance = response["availableBalance"] + response["pendingBalance"]
    return accBalance

def payment_stripe_createCard(header,chargeToken,customerId):
    url=host+'payment/stripe/createCard'
    payload={"chargeToken":chargeToken,"customerId":customerId}
    response=requests.post(url=url,json=payload,headers=header)
    return response

def payment_stripe_deleteCardForCustomer(header,cardId,customerId):
    url=host+'payment/stripe/deleteCardForCustomer'
    payload = {"cardId": cardId, "customerId": customerId}
    response = requests.post(url=url, json=payload, headers=header)
    return response

def payment_stripe_getPaymentMethodList(header,customerId):
    url=host+'payment/stripe/getPaymentMethodList'
    para={"customerId":customerId}
    response = requests.get(url=url, params=para, headers=header)
    return response

def payment_payment_list(header,customerId):
    url=host+'payment/payment/list'
    para={"customerId":customerId,"order":"desc","pageNum":1,"pageSize":10}
    response=requests.get(url=url,params=para,headers=header)
    return response

def payment_square_payments(header,payload):
    url=host+'payment/square/payments'
    response=requests.post(url=url,json=payload,headers=header)
    return response

def payment_payment_intent(guid):
    url=clientHost+'api/payment/payment/intent'
    para={"guid":guid}
    response=requests.get(url=url,params=para)
    return response

def payment_payment_payonline(guid,payload):
    url=clientHost+'api/payment/payment/payonline'
    para={"guid":guid}
    response=requests.post(url=url,json=payload,params=para)
    return response

def grooming_invoice_client_detail(guid):
    url=clientHost+'api/grooming/invoice/client/detail'
    para = {"guid": guid}
    response = requests.get(url=url, params=para)
    return response

def payment_cof_client_submit(code,payload):
    url=clientHost+'api/payment/cof/client/submit'
    para={"c":code}
    response = requests.post(url=url, json=payload, params=para)
    return response

def retail_product_list(header):
    url=host+'retail/product/list'
    para={"name":None,"order":"desc","sort":None,"pageNum":1,"pageSize":10}
    response=requests.get(url=url,params=para,headers=header)
    return response

def retail_cart_init_cart(header,businessId,staffId):
    url=host+'retail/cart/init-cart'
    payload={"businessId":businessId,"customerId":0,"saleType":"product","staffId":staffId}
    response=requests.post(url=url,json=payload,headers=header)
    return response

def retail_cart_update_cart(header,cartId,customerId):
    url=host+'retail/cart/update-cart'
    payload={"cartId":cartId,"customerId":customerId}
    response=requests.put(url=url,json=payload,headers=header)
    return response

def retail_cart_add_items(header,cartId,productId,packageId,quantity):
    url=host+'retail/cart/add-items'
    payload={"cartId":cartId,"productId":productId,"packageId":packageId,"quantity":quantity}
    response=requests.post(url=url,json=payload,headers=header)
    return response

def retail_invoice(header,cartId):
    url=host+'retail/invoice'
    payload={"cartId":cartId}
    response=requests.post(url=url,json=payload,headers=header)
    return response

def retail_invoice_detail(header,invoiceId):
    url=host+'retail/invoice/detail'
    para={"invoiceId":invoiceId}
    response=requests.get(url=url,params=para,headers=header)
    return response

def retail_cart_set_discount(header,cartId,value,valueType):
    url=host+'retail/cart/set-discount'
    payload={"cartId":cartId,"value":value,"valueType":valueType}
    response=requests.post(url=url,json=payload,headers=header)
    return response






