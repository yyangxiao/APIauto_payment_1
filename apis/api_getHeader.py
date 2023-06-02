import requests,time
from data import *
from apis.api import *

def get_header(email,pwd):
    '''
    # 登录获取token,全局header
    :param emial: 用户email
    :param pwd: 用户pwd
    :return: staffToken ，accountToken，拼接header
    '''
    token = business_account_login(email, pwd)
    accountToken = token.json()["data"]["accountToken"]
    staffToken = token.json()["data"]["staffToken"]
    header = {"account-token": accountToken, "staff-token": staffToken, "content-type": "application/json"}
    # print(email, "login success!")
    return header





