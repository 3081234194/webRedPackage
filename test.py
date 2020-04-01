import requests
import time
import datetime
import json
def getTime():
    url = "https://redpacket.tjfzys.com//activity/loadRedPacketStatus"
    local_time = int(time.time()*1000)
    print("当前时间%s" %datetime.datetime.now())
    post_data = {"devType":"android_Xiaomi_MIX","dev":"2ce3a938d7a506750b21f8b4d6926d09","actId":"7","sign":"7a81e4457d8e63f7ef122f385b39bd24","sysVer":"91","sessionID":"ed012f07e4f9db1c4e9cae72909f2242,48307DN8L","comId":"cO6UNKLe4NvJNgKBuAVEtA==","sys":"8.0.0","roomId":"693844314375589888"}
    headers = {"User-Agent":"okhttp/3.12.0"}
    res = requests.post(url=url,data=post_data,headers=headers)
    print(res.text)
    res_json = json.loads(res.text)
    print("本次请求所用时间%dms" %int(res.elapsed.total_seconds()*1000))
    if res_json["resMsg"]["resCode"]=="0000":
        str = res_json["resNum"]#获取请求时的服务器时间
        local_ms = int(str[14:17])*10#保存ms数
        str = str[0:4]+"-"+str[4:6]+"-"+str[6:8]+" "+str[8:10]+":"+str[10:12]+":"+str[12:14]#转换格式
        str = time.strptime(str, "%Y-%m-%d %H:%M:%S")#分割成结构体
        post_time = int(time.mktime(str)*1000)+local_ms#转换成时间戳
        target_time = res_json["body"]["ti"]#获取服务器上目标时间
        target_time = time.strptime(target_time, "%Y-%m-%d %H:%M:%S")#分割成结构体
        target_time = int(time.mktime(target_time)*1000)+local_ms#转换成时间戳
        target_time = target_time+(local_time+int(res.elapsed.total_seconds()*1000)-post_time)#校准目标时间
        print("校准后的目标时间%s" %target_time)
        return target_time
    else:
        print("请求服务器红包状态出错")
        print(res_json)
def getRedPackets():
    url = "https://redpacket.tjfzys.com//activity/getRedPackets.do"
    print("当前时间%s" %datetime.datetime.now())
    post_data = {"devType":"android_Xiaomi_MIX","dev":"2ce3a938d7a506750b21f8b4d6926d09","actId":"7","sign":"7a81e4457d8e63f7ef122f385b39bd24","sysVer":"91","sessionID":"ed012f07e4f9db1c4e9cae72909f2242,48307DN8L","comId":"cO6UNKLe4NvJNgKBuAVEtA==","sys":"8.0.0","roomId":"693844314375589888"}
    headers = {"User-Agent":"okhttp/3.12.0"}
    res = requests.post(url=url,data=post_data,headers=headers)
    print(res.text)


target_time = getTime()
flag = 0
while True:
    local_time = int(time.time()*1000)
    num = target_time-local_time
    print("相差时间:%s" %num)
    if flag==0 and num<100000:
        flag=1
        target_time = getTime()
    if num<=-1:#抢包开始
        getRedPackets()
        falg = 0                                                                                       
        print("当前时间%s" %datetime.datetime.now())
        time.sleep(10*60 )
        print("下一次抢包循环")
        target_time = getTime()
        continue
    if(num<40000):sleep_time=3
    if(num<=5000):sleep_time=0.002
    if(num>60000):sleep_time=29
    print("本轮等待时间:%s" %sleep_time)
    time.sleep(sleep_time)

    
