import config
from config import *
import pytest

class Test_square_retail_product_creditCard():
    '''使用credit card支付'''

    def setup_class(self) -> None:
        self.s = requests.session()
        payload = {"primaryPayType": 2}
        business_info(header, payload)
        print("primary updated to Square!")

    def teardown_class(self) -> None:
        payload = {"primaryPayType": 1}
        business_info(header, payload)
        print("primary updated to MGpay!")
        self.s.close()
        self.s = requests.session()

    def test_01_addProduct(self,set_global_data):
        cartId=retail_cart_init_cart(header,businessId,staffId).json()["data"]["id"]
        set_global_data("cartId",cartId)

        retail_cart_update_cart(header,cartId,customerId)
        productInfo=retail_product_list(header).json()["data"]["productList"][0]
        productId=productInfo["id"]

        retail_cart_add_items(header,cartId,productId,0,1)
        retail_cart_set_discount(header,cartId,20,"percentage")

        invoiceId = retail_invoice(header,cartId).json()["data"]["id"]
        set_global_data("invoiceId",invoiceId)

    def test_02_square_sellProduct_cc_successful(self, get_global_data):
        invoiceId = get_global_data("invoiceId")
        customerId = config.customerId
        customerName = config.customerName
        amount=retail_invoice_detail(header,invoiceId).json()["data"]["paymentAmount"]

        payload = {
            "amount": amount,
            "tipsAmount": 0,
            "customerId": customerId,
            "description": "",
            "invoiceId": invoiceId,
            "module": "retail",
            "paidBy": customerName,
            "signature": "",
            "staffId": staffId,
            "cardNonce": "cnon:card-nonce-ok",
            # "groomingId": groomingId,
            "useCOF": False,
            "isOnline": False,
            "isDeposit": 0
        }
        paymentResp = payment_square_payments(header, payload).json()
        # print(paymentResp)

        assert paymentResp["data"]["amount"] == amount
        assert paymentResp["data"]["status"] == "COMPLETED"
        resp = retail_invoice_detail(header, invoiceId).json()["data"]
        assert resp["paidAmount"] == amount
if __name__=="__main__":
    pytest.main()
