
import hashlib
import requests
import json
import time
import datetime
"""
config区
"""
username = "18070406411"#账号
password = "q2251682"#密码
devType = "android_Xiaomi_MAX"#机型
dev = "2ce3a938d7a506750b21f8b4d6926d09"#不变量,暂不知来源
comId = "cO6UNKLe4NvJNgKBuAVEtA=="#不变量,a101经AES加密而来
sys = "8.1.0"#安卓系统版本
sysVer = "91"#软件版本号
sessionID = 0#用户唯一标识,服务器返回
auth_sign = 0#获取包状态及抢包的sign
roomId = 0#
def main():
    loginIn(username,password)
    getInRoom(1)
    target_time = getTime(roomId)
    flag = 0
    while True:
        local_time = int(time.time()*1000)
        num = target_time-local_time
        print("相差时间:%s" %num)
        if flag==0 and num<=300000:
            flag=1
            target_time = getTime(roomId)
        if num<=-1:#抢包开始
            getRedPackets(roomId)
            flag = 0                                                                                       
            print("当前时间%s" %datetime.datetime.now())
            time.sleep(50*60 )
            print("下一次抢包循环")
            getInRoom(1)
            target_time = getTime(roomId)
            continue
        if(num<40000):sleep_time=3
        if(num<=5000):sleep_time=0.002
        if(num>60000):sleep_time=29
        print("本轮等待时间:%s" %sleep_time)
        time.sleep(sleep_time)
#登陆
def loginIn(username,password):
    global sessionID
    url = "https://app101.avictown.cc/lg/user/customer/login.do" #登陆地址
    uncode = password+"3b5949e0c26b87767a4752a276de9570"
    encode = hashlib.md5(uncode.encode("utf8")).hexdigest()#处理后的密码
    print("\033[0;32m经过处理后的密码为:%s\033[0m" %encode)
    sign = createSign(encodePass=encode,username=username)#签名
    #提交数据
    post_data = {"puskKey":"","devType":devType,"password":encode,"verifyCode":"","pVerifyCode":"","dev":dev,"phone":"","sign":sign,"sysVer":sysVer,"comId":comId,"sys":sys,"username":username}
    #提交头
    headers = {"User-Agent":"okhttp/3.12.0"}
    res = requests.post(url=url,data=post_data,headers=headers)
    if res.status_code==200:
        res_json = json.loads(res.text)
        #print(res_json)
        if res_json["resMsg"]["resCode"] =="0000":
            print("\033[0;32m登陆%s成功" %username)
            sessionID = res_json["sessionID"]
            print("成功获取并赋值到session:%s\033[0m" %sessionID)
        else:
            print("\033[0;41m服务器返回登陆失败,具体原因:\033[0m")
            print(res_json)
    else:
        print("\033[0;41m登陆失败\033[0m")
        print("等待3秒后重试")
        time.sleep(3)
        return loginIn(username,password)

#生成签名
def createSign(roomid=False,encodePass=False,username=False,anchorId=False):
    if(roomid):
        print("sign:获取红包及状态")
        code_str = "7"+comId+dev+devType+roomid+sessionID+sys+sysVer
        sign = hashlib.md5(code_str.encode("utf-8")).hexdigest()
        sign = sign+"xmzex2018!@#$%^"
        sign = hashlib.md5(sign.encode("utf-8")).hexdigest()
    elif(username):
        print("sign:登陆")
        code_str = comId+dev+devType+encodePass+sys+sysVer+username
        sign = hashlib.md5(code_str.encode("utf-8")).hexdigest()
        sign = sign+"xmzex2018!@#$%^"
        sign = hashlib.md5(sign.encode("utf-8")).hexdigest()
    elif(anchorId):
        print("sign:获取房间信息")
        code_str = anchorId+comId+dev+devType+sessionID+sys+sysVer
        sign = hashlib.md5(code_str.encode("utf-8")).hexdigest()
        sign = sign+"xmzex2018!@#$%^"
        sign = hashlib.md5(sign.encode("utf-8")).hexdigest()
    else:
        print("sign:获取视频列表")
        code_str = comId+dev+devType+"150"+sessionID+sys+sysVer#150指page_num+page_size
        sign = hashlib.md5(code_str.encode("utf-8")).hexdigest()
        sign = sign+"xmzex2018!@#$%^"
        sign = hashlib.md5(sign.encode("utf-8")).hexdigest()
    print("\033[0;32m解析得到签名为:%s\033[0m" %sign)
    return sign
#获取视频列表
def getVideolist():
    url = "https://app101.avictown.cc/lg/video/loadVideoListNew.do"
    sign = createSign()
    headers = {"User-Agent":"okhttp/3.12.0"}
    post_data = {"devType":devType,"dev":dev,"sign":sign,"pageSize":"50","sysVer":"91","sessionID":sessionID,"comId":comId,"sys":sys,"pageNum":"1"}
    res = requests.post(url=url,data=post_data,headers=headers)
    if res.status_code==200:
        res_json = json.loads(res.text)
        if res_json["resMsg"]["resCode"]=="0000":
            print("\033[0;32m获取列表成功\033[0m")
            return res_json["body"]["rows"]
        else:
            print("服务器返回获取列表失败")
            print("服务器返回的消息:%s" %res_json["resMsg"]["resDesc"])
            exit()
    else:
            print("获取列表失败，3秒后重试")
            time.sleep(3)
            return getVideolist()
#决定并进入房间,传参为视频列表
def getAnchorId(videoList,index=0):
    watch_num = []#观众数
    for info in videoList:
        watch_num.append(int(info["on"]))
    watch_num0 = watch_num#原排序
    watch_num.sort(reverse=True)
    #print("观众数排列%s" %watch_num)
    target_num = watch_num[index]
    index_num = watch_num0.index(target_num)#排列数在视频列表的位置
    anchorId = videoList[index_num]["aid"]
    print("目标昵称:%s" %videoList[index_num]["an"])
    print("房间观看人数:%s" %target_num)
    return anchorId 
#获取服务器时间戳
def getTime(roomid):
    global auth_sign
    auth_sign = createSign(roomid=roomid)
    local_time = int(time.time()*1000)
    print("当前时间%s" %datetime.datetime.now())
    url = "https://redpacket.tjfzys.com//activity/loadRedPacketStatus"
    post_data = {"devType":devType,"dev":dev,"actId":"7","sign":auth_sign,"sysVer":sysVer,"sessionID":sessionID,"comId":comId,"sys":sys,"roomId":roomid}
    headers = {"User-Agent":"okhttp/3.12.0"}
    res = requests.post(url=url,data=post_data,headers=headers)
    print(res.text)
    if res.status_code==200:
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
            target_time = target_time+(local_time-post_time+int(res.elapsed.total_seconds()*1000*0.8))#校准目标时间
            print("校准后的目标时间%s" %target_time)
            return target_time
        else:
            print("请求服务器红包状态出错")
            print(res_json)
    else:
        print("请求时间失败,等待3S后重试")
        time.sleep(3)
        return getTime(roomid)
#获取房间id
def getRoomId(anchorId):
    sign = createSign(anchorId=anchorId)
    url = "https://app101.avictown.cc/lg/video/loadRoomInfo.do"
    headers = {"User-Agent":"okhttp/3.12.0"}
    post_data = {"devType":devType,"dev":dev,"sign":sign,"sysVer":sysVer,"sessionID":sessionID,"comId":comId,"anchorId":anchorId,"sys":sys}
    res = requests.post(url=url,data=post_data,headers=headers)
    if res.status_code==200:
        res_json = json.loads(res.text)
        if res_json["resMsg"]["resCode"]=="0000":
            #print(res_json)
            wallet = int(res_json["body"]["um"]["ex"])/100
            print("\033[30;43m钱包余额%s\033[0m" %wallet)
            print("进入%s的房间,房间号:%s" %(res_json["body"]["am"]["nn"],res_json["body"]["am"]["ri"]))
            return res_json["body"]["am"]["ri"]
    else:
        print("获取房间id失败,等待3S后重试")
        time.sleep(3)
        return getRoomId(anchorId)
#获取红包
def getRedPackets(roomid):
    url = "https://redpacket.tjfzys.com//activity/getRedPackets.do"
    post_data = {"devType":devType,"dev":dev,"actId":"7","sign":auth_sign,"sysVer":sysVer,"sessionID":sessionID,"comId":comId,"sys":sys,"roomId":roomid}
    headers = {"User-Agent":"okhttp/3.12.0"}
    res = requests.post(url=url,data=post_data,headers=headers)
    if res.status_code==200:
        res_json = json.loads(res.text)
        if res_json["resMsg"]["resCode"]=="0000":
            if res_json["body"]["su"]=="1":
                money = int(res_json["body"]["am"])/100
                print("抢到红包了,金额:%f" %money)
            else:
                print("未抢到红包,状态码:%s" %res_json["body"]["su"])
                print(res_json)
        else:
            print("抢包失败,服务器返回信息:%s" %res_json["resMsg"]["resDesc"])
    else:
        print("抢包失败,检查网络")
        print(res.text)
#获取视频列表决定进入人数排序的哪一个房间
def getInRoom(index=0):
    global roomId
    videolist = getVideolist()
    anchorId = getAnchorId(videoList=videolist,index=index)
    roomId = getRoomId(anchorId)
    return roomId

main()