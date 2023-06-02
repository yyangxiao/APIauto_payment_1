#不同环境的host
t2='https://gate-grey-go.t2.moego.pet/api/'
ct2='https://gate-grey-client.t2.moego.pet/'
s1='https://go.s1.moego.pet/api/'
prod='https://go.moego.pet/api/'


# test account info
host=t2
clientHost=ct2
email='yangxiao@mymengshi.com'
pwd='12345678'
# lastBizId=100741 # optional

#smart list 筛选条件
smartListParam={
  "queries": {
    "keyword": ""
  },
  "filters": {
    "type": "TYPE_AND",
    "filters": [
      {
        "property": "client_status",
        "value": "active",
        "values": [],
        "operator": "OPERATOR_EQUAL"
      }
    ]
  },
  "sort": {
    "order": "asc",
    "property": "first_name"
  },
  "pageNum": 1,
  "pageSize": 10
}

# customize rate:
conlineFeeRate=3.4
conlineCents=30

signature="https://moegonew.s3-us-west-2.amazonaws.com/Public/Uploads/16842292583614b2be39784d11ac0b8f99c4b54b42.processing_fee_signature_100741_1684229258482"
