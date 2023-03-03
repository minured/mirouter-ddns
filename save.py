import redis
from datetime import datetime
import json


REDIS_KEY = "ddns_ip"


def connectRedis():
    with open("./config.json") as fp:
        redisDB = json.load(fp)

    redisCon: redis.Redis = redis.Redis(host=redisDB["host"], port=redisDB["port"],
                                        password=redisDB["redisPwd"], db=redisDB["db"], decode_responses=True)

    return redisCon


def saveIP(ip):
    redisCon = connectRedis()
    latest = redisCon.lindex(REDIS_KEY, 0) or "ip_time"
    latestIP = latest.split("_")[0]
    if (ip != latestIP):
        timestamp = str(datetime.timestamp(datetime.now()))[0:10]
        value = "{}_{}".format(ip, timestamp)
        redisCon.lpush(REDIS_KEY, value)
        print("{} saved!".format(value))
    else:
        print("ip existed, skip")
