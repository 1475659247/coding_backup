import redis 
r = redis.Redis(host="127.0.0.1",port=6379,db=0,password="")
re = r.get("ip_status")
if re == None:
    r.setex("ip_status","switching",120)
    print("no")
else:
    print("yes")
    print(re)


