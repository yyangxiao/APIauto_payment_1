from config import *
from apis.api_createAppt import *
import pytest,apis

class Test_noShow_creditCard():
    '''使用credit card支付no show'''

    def setup_class(self) -> None:
        self.s = requests.session()

    def teardown_class(self) -> None:
        self.s.close()

    def test_acreateAppt(self,set_global_data):
        groomingId = create_appt(header)
        set_global_data("groomingId", groomingId)
        pup = grooming_appointment_detail_pup(header, groomingId).json()

        # cancel且mark as no show
        grooming_appointment_cancel(header,groomingId,1,"api test noShow")

        customerId = pup["data"]["customerId"]
        set_global_data("customerId", customerId)
        customerName = pup["data"]["groomingCustomerInfo"]["firstName"] + ' ' + pup["data"]["groomingCustomerInfo"][
            "lastName"]
        set_global_data("customerName", customerName)
        #
        # invoiceDetail = grooming_invoice_order_detail(header, invoiceId).json()
        # amount = invoiceDetail["remainAmount"]
        # set_global_data("amount", amount)
        oriAccountBalance=payment_stripe_getConnectedInfo(header)
        set_global_data("oriAccountBalance", oriAccountBalance)

    def test_noShow_creditCard(self, get_global_data):
        noShowAmount=50
        groomingId=get_global_data("groomingId")
        noShowResp=grooming_invoice_noshow(header,noShowAmount,groomingId).json()
        invoiceId = noShowResp["data"]["id"]
        customerId = get_global_data("customerId")
        customerName = get_global_data("customerName")
        # amount = get_global_data("amount")
        stripePaymentMethod = 1
        processingFee = payment_payment_processingFee(header, noShowAmount, stripePaymentMethod).json()["processingFee"]
        paymentAmount = noShowAmount + processingFee
        payload = {
            "amount": noShowAmount,
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
            # "isDeposit": 0,
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
        # try:
        #     # 断言--支付金额、invoice中的convenience fee
        #     assert resp["paidAmount"] == paymentAmount
        #     assert resp["convenienceFee"] == processingFee
        # except:
        #     print(invoiceId,"payment error!")
        # 断言--支付金额、invoice中的convenience fee
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
    pytest.main()