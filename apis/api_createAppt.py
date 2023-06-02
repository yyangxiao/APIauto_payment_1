import config
from apis.api_getHeader import *
from config import *

def create_appt(header):
    '''
    自动createAppt
    :param header:用户登录后的header
    :return:groomingId
    '''
    # 取当前时间为appt start time-----------------------------
    apptTime = time.localtime()  # 返回为'time.struct_time' 是named tuple, 可通过 索引obj[*] 或者 属性obj.attr 提取属性值
    hour = apptTime.tm_hour
    min = apptTime.tm_min
    startTime = hour * 60 + min
    apptDate = time.strftime("%Y-%m-%d", time.localtime())
    # print(startTime,apptDate)

    # 取到第一个customer--------------------------------------
    customerId = config.customerId

    # 取第一个pet--------------------------------------------
    petInfo = customerInfo["petList"][0]
    petId = petInfo["petId"]
    # print(customerId,customerInfo["firstName"],petId)

    # 取第一个service、add on----------------------------------
    serInfo = grooming_services(customerId, petId, header).json()

    serviceInfo = serInfo["data"][0]["petServices"][0]
    serviceId = serviceInfo["id"]
    servicePrice = serviceInfo["price"]
    serviceDuration = serviceInfo["duration"]

    addOnInfo = serInfo["data"][-1]["petServices"][0]
    addOnId = addOnInfo["id"]
    addOnPrice = addOnInfo["price"]
    addOnDuration = addOnInfo["duration"]
    # print(serviceInfo)

    # 取第一个staff--------------------------------------------
    staffList = business_staff_list(header).json()
    staffInfo = staffList["data"][0]
    staffId = staffInfo["id"]

    # 创建appt-----------------------------------------------
    payload = {
        "petServices": [
            {
                "serviceType": 1,
                "petId": petId,
                "scopeTypePrice": 2,  # -------?
                "startTime": startTime,
                "servicePrice": servicePrice,
                "serviceId": serviceId,
                "serviceTime": serviceDuration,
                "staffId": staffId,
                "scopeTypeTime": 2,  # -------?
                "star": False
            },
            {
                "serviceType": 2,
                "petId": petId,
                "scopeTypePrice": 2,
                "startTime": startTime + serviceDuration,
                "servicePrice": addOnPrice,
                "serviceId": addOnId,
                "serviceTime": addOnDuration,
                "staffId": staffId,
                "scopeTypeTime": 2,
                "star": False
            }
        ],
        "source": 22018,
        "appointmentDateString": apptDate,
        "ticketComments": "apiCreated",
        "appointmentStartTime": startTime,
        "customerId": customerId,
        "colorCode": "#000000",
        "alertNotes": "apiAlert"
    }

    appt = grooming_appointment_POST(payload, header).json()
    groomingId = appt["data"]["id"]
    return groomingId





