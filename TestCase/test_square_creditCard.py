import config
from config import *
from apis.api_createAppt import *
import pytest,apis

class Test_square_creditCard():
    '''使用credit card支付'''

    def setup_class(self) -> None:
        self.s = requests.session()
        payload={"primaryPayType":2}
        business_info(header,payload)
        print("primary updated to Square!")

    def teardown_class(self) -> None:
        payload = {"primaryPayType": 1}
        business_info(header, payload)
        print("primary updated to MGpay!")
        self.s.close()

    def test_createAppt(self,set_global_data):
        groomingId = create_appt(header)
        set_global_data("groomingId", groomingId)
        pup = grooming_appointment_detail_pup(header, groomingId).json()
        invoiceId = pup["data"]["invoiceId"]
        set_global_data("invoiceId", invoiceId)
        customerId = config.customerId
        set_global_data("customerId", customerId)
        customerName = pup["data"]["groomingCustomerInfo"]["firstName"] + ' ' + pup["data"]["groomingCustomerInfo"][
            "lastName"]
        set_global_data("customerName", customerName)

        invoiceDetail = grooming_invoice_order_detail(header, invoiceId).json()
        amount = invoiceDetail["remainAmount"]
        set_global_data("amount", amount)

        oriAccountBalance=payment_stripe_getConnectedInfo(header)
        set_global_data("oriAccountBalance", oriAccountBalance)

    def test_square_creditCard(self, get_global_data):
        groomingId=get_global_data("groomingId")
        invoiceId = get_global_data("invoiceId")
        customerId = get_global_data("customerId")
        customerName = get_global_data("customerName")
        amount = get_global_data("amount")

        payload = {
            "amount": amount,
            "tipsAmount": 0,
            "customerId": customerId,
            "description": "",
            "invoiceId": invoiceId,
            "module": "grooming",
            "paidBy": customerName,
            "signature": "",
            "staffId": staffId,
            "cardNonce": "cnon:card-nonce-ok",
            "groomingId": groomingId,
            "useCOF": False,
            "isOnline": False,
            "isDeposit": 0
        }
        paymentResp = payment_square_payments(header, payload).json()
        print(paymentResp)

        assert paymentResp["data"]["amount"] == amount
        assert paymentResp["data"]["status"] == "COMPLETED"
        resp = grooming_invoice_order_detail(header, invoiceId).json()
        assert resp["paidAmount"] == amount
        # 判断appt是否自动finished
        pup = grooming_appointment_detail_pup(header, get_global_data("groomingId")).json()
        assert pup["data"]["status"] == 3  # finished

if __name__=="__main__":
    pytest.main()