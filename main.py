import requests
from datetime import datetime
from random import randint
import hashlib
import json


# TODO 之后在页面读取
deviceId = ""
nonceType = 0
pwdKey = "a2ffa5c9be07488bbb04a3a47d3c5f6a"
password = ""
adminUrl = ""


def initialize():
    global deviceId, password, adminUrl

    with open("./config.json") as fp:
        config = json.load(fp)

        deviceId = config["deviceId"]
        password = config["password"]
        adminUrl = config["adminUrl"]



def generateNonce():
    timeStamp = str(datetime.timestamp(datetime.now()))[0:10]
    randomNum = randint(1, 9999)
    return "{}_{}_{}_{}".format(nonceType, deviceId, timeStamp, randomNum)


def encryptPwd(nonce):
    firstEncrypt = hashlib.sha1((password + pwdKey).encode("utf8")).hexdigest()
    secondEncrypt = hashlib.sha1(
        (nonce + firstEncrypt).encode("utf8")).hexdigest()
    return secondEncrypt


def login():
    loginUrl = "{}/cgi-bin/luci/api/xqsystem/login".format(adminUrl)
    nonce = generateNonce()
    data = {
        "username": "admin",
        "password": encryptPwd(nonce),
        "logtype": 2,
        "nonce": nonce
    }
    res = requests.post(url=loginUrl, data=data)
    if (res.status_code == 200):
        return res.json()["token"]
    else:
        print("LOGIN ERROR", res.status_code, res.text)
        return None


def getAddress():
    token = login()
    url = "{}/cgi-bin/luci/;stok={}/api/xqnetwork/pppoe_status".format(adminUrl, token)
    res = requests.get(url)
    if (res.status_code == 200):
        res = res.json()
        
    print(res["ip"]["address"])


def main():
    initialize()
    getAddress()


if __name__ == "__main__":
    main()
