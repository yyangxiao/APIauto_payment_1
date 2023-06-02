import config
from config import *
import pytest

class Test_retail_product_creditCard():
    '''使用credit card支付'''

    def setup_class(self) -> None:
        self.s = requests.session()

    def teardown_class(self) -> None:
        self.s.close()

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

        oriAccountBalance = payment_stripe_getConnectedInfo(header)
        set_global_data("oriAccountBalance", oriAccountBalance)

    def test_02_sellProduct_cc_successful(self, get_global_data):
        invoiceId = get_global_data("invoiceId")
        customerId = config.customerId
        customerName = config.customerName
        amount=retail_invoice_detail(header,invoiceId).json()["data"]["paymentAmount"]

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
            "module": "retail",
            "paidBy": customerName,
            "signature": "",
            "staffId": staffId,
            "stripePaymentMethodId": "",
            "stripePaymentMethod": 1,
            "isOnline": False,
            "chargeToken": "tok_visa",
            "saveCard": False,
            "isDeposit": 0,
            "addProcessingFee": False
        }
        paymentResp = payment_payment_createAndConfirm(header, payload, businessId).json()
        print(paymentResp)
        # 轮询5次
        for i in range(1, 6):
            resp = retail_invoice_detail(header, invoiceId).json()["data"]
            if resp["status"] == 'completed':
                print(i, invoiceId, ":payment success!")
                break
            if resp["status"] == 'failed':
                print(i, invoiceId, ":payment failed!")
                break
            elif i == 5 and resp["status"] == 'processing':
                print(i, invoiceId, "Something wrong!")

        # print(resp["status"])

        assert resp["paidAmount"] == amount
        # print(resp["status"],resp["paidAmount"])
        # assert resp["convenienceFee"] == processingFee


        # 取本次payment的paymentId、applicationFee
        clientPayments=payment_payment_list(header,customerId).json()
        applicationFee=clientPayments["data"]["paymentList"][0]["processingFee"]
        oriAccountBalance=get_global_data("oriAccountBalance")
        accountBalance=oriAccountBalance+amount-applicationFee
        # print(accountBalance,type(accountBalance))
        accBalance='%.2f'%accountBalance
        newAccountBalance=payment_stripe_getConnectedInfo(header)
        newAccBalance = '%.2f' % newAccountBalance
        assert accBalance == newAccBalance
if __name__=="__main__":
    pytest.main()
