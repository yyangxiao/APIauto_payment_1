from config import *
from apis.api_createAppt import *
import pytest

class Test_payment_creditCard():
    '''使用credit card支付'''

    def setup_class(self) -> None:
        self.s = requests.session()

    def teardown_class(self) -> None:
        self.s.close()

    def test_01_acreateAppt(self,set_global_data):
        groomingId = create_appt(header)
        set_global_data("groomingId", groomingId)
        pup = grooming_appointment_detail_pup(header, groomingId).json()
        invoiceId = pup["data"]["invoiceId"]
        set_global_data("invoiceId", invoiceId)

        invoiceDetail = grooming_invoice_order_detail(header, invoiceId).json()
        amount = invoiceDetail["remainAmount"]
        set_global_data("amount", amount)

        oriAccountBalance=payment_stripe_getConnectedInfo(header)
        set_global_data("oriAccountBalance", oriAccountBalance)

    def test_02_cc_successful(self, get_global_data):
        invoiceId = get_global_data("invoiceId")
        amount = get_global_data("amount")

        stripePaymentMethod = 1
        processingFee = payment_payment_processingFee(header, amount, stripePaymentMethod).json()["processingFee"]
        paymentAmount = amount + processingFee
        payload = {
            "amount": amount,
            "tipsAmount": 0,
            "cardNumber": "1111",
            "cardType": "Visa",
            "customerId": customerId,
            "description": "",
            "expMonth": "11",
            "expYear": "2024",
            "invoiceId": invoiceId,
            "methodId": 1,
            "module": "grooming",
            "paidBy": customerName,
            "signature": "",
            "staffId": staffId,
            "stripePaymentMethodId": "",
            "stripePaymentMethod": 1,
            "isOnline": False,
            "chargeToken": "tok_visa",
            "saveCard": False,
            "isDeposit": 0,
            "addProcessingFee": True
        }
        paymentResp = payment_payment_createAndConfirm(header, payload, businessId).json()
        print(paymentResp)

        # 轮询5次
        for i in range(1, 6):
            resp = grooming_invoice_order_detail(header, invoiceId).json()
            if resp["status"] == 'completed':
                print(i, invoiceId, ":payment success!")
                break
            if resp["status"] == 'failed':
                print(i, invoiceId, ":payment failed!")
                break
            elif i == 5 and resp["status"] == 'processing':
                print(i, invoiceId, "Something wrong!")

        assert resp["paidAmount"] == paymentAmount
        assert resp["convenienceFee"] == processingFee


        # 取本次payment的paymentId、applicationFee
        clientPayments=payment_payment_list(header,customerId).json()
        applicationFee=clientPayments["data"]["paymentList"][0]["processingFee"]
        oriAccountBalance=get_global_data("oriAccountBalance")
        accountBalance=oriAccountBalance+paymentAmount-applicationFee
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
    pytest.main(['-vs','test_payment_creditCard.py'])
