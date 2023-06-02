from config import *
from data import *
from apis.api_stripePaymentIntent import *
from apis.api_createAppt import *
import pytest,apis

class Test_cardAuth():
    '''测试card authentication'''

    def setup_class(self) -> None:
        self.s = requests.session()
        # 打开cardAuth
        payload={"businessId":businessId,"cardAuthEnable":1}
        payment_setting_info_put(header,payload)

    def teardown_class(self) -> None:
        self.s.close()

    def test_addManually(self,set_global_data):
        paymentMethodList=[]
        set_global_data("paymentMethodList",paymentMethodList)
        # add manually--添加fraud卡
        chargeToken = "tok_radarBlock"
        response=payment_stripe_createCard(header, chargeToken, customerId).json()
        assert response["code"] == 70021
        assert "authentication failed" in response["message"]
        assert not response["success"]

        # add manually--添加3DS卡， 无测试token

        # add manually--添加insufficient funds卡
        chargeToken = "tok_visa_chargeDeclinedInsufficientFunds"
        response = payment_stripe_createCard(header, chargeToken, customerId).json()
        assert response["code"] == 70021
        assert "authentication failed" in response["message"]
        assert not response["success"]

        # add manually--添加正常卡
        chargeToken = "tok_discover"
        response = payment_stripe_createCard(header, chargeToken, customerId).json()
        cardId=response["id"]
        customerCardInfo = payment_stripe_getPaymentMethodList(header, customerId).json()["data"]
        cardIdList = []
        for item in customerCardInfo:
            cardIdList.append(item["id"])
        # 判断卡片是否添加成功
        assert cardId in cardIdList
        paymentMethodList.append(cardId)

    def test_cardAuthLink(self,get_global_data):
        paymentMethodList=get_global_data("paymentMethodList")

        # 生成code
        link=payment_cof_code(header,customerId).json()["link"].lstrip('/')
        cofLink=clientHost+link
        llist=link.split('c=')
        code=llist[-1]

        # cof request--添加fraud卡
        chargeToken = "tok_radarBlock"
        payload={
            "c":code,
            "email":customerEmail,
            "firstName":firstName,
            "lastName":lastName,
            "phone":customerPhone,
            "stripeToken":chargeToken
        }

        response=payment_cof_client_submit(code,payload).json()
        assert response["code"] == 70021
        assert "authentication failed" in response["message"]
        assert not response["success"]

        # cof request--添加debit卡
        chargeToken = "tok_mastercard_debit"
        payload = {
            "c": code,
            "email": customerEmail,
            "firstName": firstName,
            "lastName": lastName,
            "phone": customerPhone,
            "stripeToken": chargeToken
        }

        response=payment_cof_client_submit(code,payload).text
        cardId = response
        customerCardInfo = payment_stripe_getPaymentMethodList(header, customerId).json()["data"]
        cardIdList = []
        for item in customerCardInfo:
            cardIdList.append(item["id"])
        # 判断卡片是否添加成功
        assert cardId in cardIdList


if __name__=="__main__":
    pytest.main()