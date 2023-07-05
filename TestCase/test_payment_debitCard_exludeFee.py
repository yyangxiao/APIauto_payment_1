from config import *
from apis.api_createAppt import *
import pytest,apis

class Test_payment_debitCard_excludeFee():
    '''使用credit card支付'''

    def setup_class(self) -> None:
        self.s = requests.session()

    def teardown_class(self) -> None:
        self.s.close()

    def test_00_createAppt(self,set_global_data):
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

    def test_01_debit_excludeFee_successful(self, get_global_data):
        invoiceId = get_global_data("invoiceId")
        customerId = get_global_data("customerId")
        customerName = get_global_data("customerName")
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
            "chargeToken": "tok_visa_debit",
            "saveCard": True,
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

        # 断言--支付金额、invoice中的convenience fee
        assert resp["paidAmount"] == paymentAmount-processingFee
        assert resp["paymentSummary"]["payments"][0]["cardFunding"] == 'debit'
        assert resp["status"] == "completed"

        # 判断appt是否自动finished
        pup = grooming_appointment_detail_pup(header, get_global_data("groomingId")).json()
        assert pup["data"]["status"] == 3  # finished
        # assert resp["convenienceFee"] == processingFee
        # 取本次payment的paymentId、applicationFee
        # paymentId=resp["paymentSummary"]["payments"][0]["id"]
        clientPayments=payment_payment_list(header,customerId).json()
        applicationFee=clientPayments["data"]["paymentList"][0]["processingFee"]
        oriAccountBalance=get_global_data("oriAccountBalance")
        accountBalance=oriAccountBalance+paymentAmount-processingFee-applicationFee
        accBalance = '%.2f' % accountBalance
        newAccountBalance = payment_stripe_getConnectedInfo(header)
        newAccBalance = '%.2f' % newAccountBalance
        # 断言--账户balance
        assert accBalance == newAccBalance
if __name__=="__main__":
    pytest.main(['-vs','test_payment_debitCard_excludeFee.py'])