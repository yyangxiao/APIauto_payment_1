from config import *
from data import *
from apis.api_stripePaymentIntent import *
from apis.api_createAppt import *
import pytest

class Test_payOnline_debitCard():
    '''使用debit card支付'''

    def setup_class(self) -> None:
        self.s = requests.session()

    def teardown_class(self) -> None:
        self.s.close()

    def test_createAppt(self,set_global_data):
        groomingId = create_appt(header)
        set_global_data("groomingId", groomingId)
        pup = grooming_appointment_detail_pup(header, groomingId).json()
        invoiceId = pup["data"]["invoiceId"]
        set_global_data("invoiceId", invoiceId)
        customerId = pup["data"]["customerId"]
        set_global_data("customerId", customerId)
        customerName = pup["data"]["groomingCustomerInfo"]["firstName"] + ' ' + pup["data"]["groomingCustomerInfo"][
            "lastName"]
        set_global_data("customerName", customerName)

        invoiceDetail = grooming_invoice_order_detail(header, invoiceId).json()
        amount = invoiceDetail["remainAmount"]
        set_global_data("amount", amount)

        oriAccountBalance=payment_stripe_getConnectedInfo(header)
        set_global_data("oriAccountBalance", oriAccountBalance)


    def test_payOnline_debitCard_excludeFee(self, get_global_data):
        invoiceId = get_global_data("invoiceId")
        customerId = get_global_data("customerId")
        customerName = get_global_data("customerName")
        amount = get_global_data("amount")

        stripePaymentMethod = 1
        processingFee = payment_payment_processingFee(header, amount, stripePaymentMethod).json()["processingFee"]
        paymentAmount = amount + processingFee

        requiredProcessingFee = True
        guid = grooming_invoice_client_url(header, invoiceId, requiredProcessingFee).json()["guid"]
        paymentLink =clientHost+'payment/online/'+guid
        print(paymentLink)

        paymentIntendId=payment_payment_intent(guid).json()["data"]["intendId"]
        # secretKey=payment_payment_intent(guid).json()["data"]["secretKey"]

        payload = {
            "amount": amount,
            "tipsAmount": 0,
            "customerId": customerId,
            "description": "",
            "invoiceId": invoiceId,
            "method":"Credit card",
            "methodId": 1,
            "module": "grooming",
            "paidBy": customerName,
            "paymentIntentId": paymentIntendId,
            "stripePaymentMethod": 1,
            "isOnline": True,
            "saveCard": False,
            "signature":"",
            "addProcessingFee": True
        }
        paymentResp = payment_payment_payonline(guid,payload).json()
        print(paymentResp)

        stripeClientSecret=paymentResp["data"]["stripeClientSecret"]
        returnUrl=paymentLink

        payloadStripe = {
            "key": "pk_test_iE6oFDNcmBgkuWlPFWuShPfo",
            "client_secret":stripeClientSecret,
            "expected_payment_method_type": "card",
            "payment_method_data[type]":"card",
            "use_stripe_sdk": True,
            "payment_method_data[card][token]":"tok_visa_debit",
            "return_url":returnUrl
        }

        onlinePayResp=stripe_payment_intents(paymentIntendId,payloadStripe)
        print(onlinePayResp.text)

        # client-invoice-detail接口轮询5次
        for i in range(1, 6):
            resp = grooming_invoice_client_detail(guid).json()["invoiceInfo"]
            if resp["status"] == 'completed':
                print(i, invoiceId, ":payment success!")
                break
            if resp["status"] == 'failed':
                print(i, invoiceId, ":payment failed!")
                break
            elif i == 5 and resp["status"] == 'processing':
                print(i, invoiceId, "Something wrong!")

        assert resp["paidAmount"] == paymentAmount-processingFee

        respB=grooming_invoice_order_detail(header,invoiceId).json()
        assert respB["paymentSummary"]["payments"][0]["cardFunding"] == 'debit'
        assert respB["paymentSummary"]["payments"][0]["isOnline"]
        assert resp["status"] == "completed"

        # 判断appt是否自动finished
        pup = grooming_appointment_detail_pup(header, get_global_data("groomingId")).json()
        assert pup["data"]["status"] == 3  # finished
        # assert resp["convenienceFee"] == processingFee
        #
        #
        # 取本次payment的paymentId、applicationFee
        clientPayments=payment_payment_list(header,customerId).json()
        applicationFee=clientPayments["data"]["paymentList"][0]["processingFee"]
        oriAccountBalance=get_global_data("oriAccountBalance")
        accountBalance=oriAccountBalance+paymentAmount-processingFee-applicationFee
        accBalance='%.2f'%accountBalance
        newAccountBalance=payment_stripe_getConnectedInfo(header)
        newAccBalance = '%.2f' % newAccountBalance

        # try:
        #     assert accBalance == newAccBalance+1
        # except:
        #     print("Account balance error!")
        # 断言--账户balance
        assert accBalance == newAccBalance
if __name__=="__main__":
    pytest.main()