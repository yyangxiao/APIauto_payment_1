from apis.api_getHeader import *

header=get_header(email,pwd)
info_v2 = business_account_info_v2(header).json()

staffId = info_v2["data"]["staff"]["staffId"]

businessId =info_v2["data"]["business"]["id"]

customerList = customer_smartList(header).json()
customerInfo = customerList["clientPage"]["dataList"][9]
customerId = customerInfo["customerId"]
firstName=customerInfo["firstName"]
lastName=customerInfo["lastName"]
customerName=firstName+' '+lastName
customerEmail=customerInfo["email"]
customerPhone=customerInfo["phoneNumber"]
print(customerPhone)



