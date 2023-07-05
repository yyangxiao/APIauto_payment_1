from apis.api_createAppt import *
import pytest

class Test_cof_debitCard_excludeFee():
    '''使用COF-credit card支付'''

    def setup_class(self) -> None:
        self.s = requests.session()

    def teardown_class(self) -> None:
        self.s.close()

    def test_01_addCard(self,set_global_data):
        chargeToken="tok_mastercard_debit"
        cardId=payment_stripe_createCard(header,chargeToken,customerId).json()["id"]
        set_global_data("cardId",cardId)
        # print(cardId)
        customerCardInfo=payment_stripe_getPaymentMethodList(header,customerId).json()["data"]
        cardIdList=[]
        for item in customerCardInfo:
            cardIdList.append(item["id"])
        # 判断卡片是否添加成功
        assert cardId in cardIdList
        print("add card:", cardId)

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


    def test_02_debitCard_excludeFee(self, get_global_data):
        invoiceId = get_global_data("invoiceId")
        amount = get_global_data("amount")
        cardId=get_global_data("cardId")

        customerCardInfo = payment_stripe_getPaymentMethodList(header, customerId).json()["data"][0]
        cardNumber=customerCardInfo["card"]["last4"]
        cardTYpe=customerCardInfo["card"]["brand"]
        exp_month=customerCardInfo["card"]["exp_month"]
        exp_year=customerCardInfo["card"]["exp_year"]

        stripePaymentMethod = 1
        processingFee = payment_payment_processingFee(header, amount, stripePaymentMethod).json()["processingFee"]
        paymentAmount = amount + processingFee
        payload = {
              "amount": amount,
              "tipsAmount": 0,
              "cardNumber": cardNumber,
              "cardType": cardTYpe,
              "customerId": customerId,
              "description": "",
              "expMonth": exp_month,
              "expYear": exp_year,
              "invoiceId": invoiceId,
              "methodId": 1,
              "module": "grooming",
              "paidBy": customerName,
              "signature": "",
              "staffId": staffId,
              "stripePaymentMethodId": cardId,
              "stripePaymentMethod": 2,
              "isOnline": False,
              "chargeToken": cardId,
              "saveCard": False,
              "isDeposit": 0,
              "addProcessingFee": True
        }
        paymentResp = payment_payment_createAndConfirm(header, payload, businessId).json()
        # print(paymentResp)

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

        assert resp["paidAmount"] == paymentAmount-processingFee
        # assert resp["convenienceFee"] == processingFee
        assert resp["status"] == "completed"

        # 判断appt是否自动finished
        pup = grooming_appointment_detail_pup(header, get_global_data("groomingId")).json()
        assert pup["data"]["status"] == 3  # finished

        # 取本次payment的paymentId、applicationFee
        clientPayments = payment_payment_list(header, customerId).json()
        applicationFee = clientPayments["data"]["paymentList"][0]["processingFee"]
        oriAccountBalance = get_global_data("oriAccountBalance")
        accountBalance = oriAccountBalance + amount- applicationFee
        accBalance = '%.2f' % accountBalance
        newAccountBalance = payment_stripe_getConnectedInfo(header)
        newAccBalance = '%.2f' % newAccountBalance
        assert accBalance == newAccBalance

        # 删除本次添加的卡片
        payment_stripe_deleteCardForCustomer(header, cardId, customerId)
        print("deleted card:", cardId)

if __name__=="__main__":
    pytest.main()