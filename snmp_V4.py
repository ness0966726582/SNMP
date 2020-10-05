'''
功能一
從Data4.txt取得snmp資訊,文檔包含以下
Community + IP + Port + OID + location + sensor_name (直接在文字檔內新增利用Tab鍵分隔)

功能二
定時擷取文檔內的OID

功能三
判斷溫度的數值做2次處理confirm_Value()

功能四
處理完後彙整上傳all_info---->額外生成兩個1.感測數值2.取樣時間

功能五
開啟網頁open_URL()

功能六
定時上傳tick()Sendsheet()

功能七
未啟用bar100()
未啟用陣列上傳
未啟用輸出Log檔
未啟用line告警

'''
from time import *
import time;  # 引入time模块

import os
from apscheduler.schedulers.blocking import BlockingScheduler
from pysnmp.hlapi import *

import sys
file_name = 'Data4.txt'
count = 0    #計數變量
result = []
varCommunity = ""
IP = ""
varPort = ""
oid = ""
oidValue = ""  #取得OID全資訊(需在處理)
location = ""
sensor_name = ""
time_now = ""

all_info = "" #全部資訊逐行上傳至googlesheet

def reset():
    global count,result,varCommunity,IP,varPort,oid
    ########
    #全歸零#
    ########
    count = 0    
    result = []
    varCommunity = ""
    IP = ""
    varPort = ""
    oid = ""
    oidValue =""
    location = ""
    sensor_name = ""
    time_now = ""
    all_info = ""

def now():
        global time_now
        #nowD = time.strftime("%Y-%m-%d", time.localtime())
        nowH = time.strftime('%H', time.localtime())
        nowM = time.strftime('%M', time.localtime())
        #nowDate = [str(nowD)]
        time_now = str([str(nowH)+":"+str(nowM)])[2:7]
        #print(time.strftime("%Y", time.localtime())+"年"+time.strftime("%m", time.localtime())+"月"+time.strftime("%d", time.localtime())+"日")
        #print("nowDate:",nowDate)
        #print("nowTime",nowTime)
        #return [nowDate,nowTime]

def get_TXT():
    global count,result,varCommunity,IP,varPort,oid,location,sensor_name
    ###############
    #取得每行文字檔資料#
    ###############
    with open(file_name,'r',encoding='utf-8') as f:
        for line in f:
            result.append(list(line.strip('\n').split(',')))
    #檢視取得的資料
    #print(result)

    ###################
    #data.txt內使用行數#
    ###################
    file_dirs = file_name
    filename = open(file_dirs,'r',encoding='utf-8')        #以只读方式打开文件
    file_contents = filename.read()       #读取文档内容到file_contents
    for file_content in file_contents:    #统计文件内容中换行符的数目
        if file_content == '\n':
            count += 1
    if file_contents[-1] != '\n':         #当文件最后一个字符不为换行符时，行数+1
        count += 1
    #print('文件%s總共有%d行' % (file_dirs, count))
        
    #########
    #資料處理#
    #########
    for i in range(1,count):
        i+1
        #print(str(result[i]))
        keep = str(result[i]).split("\\t")
        #print("轉移暫存"+str(keep))
        
        varCommunity = str(keep[0]).strip("['")
        IP = str(keep[1])
        varPort = str(keep[2])
        oid = str(keep[3])
        location =str(keep[4])
        sensor_name =str((keep[5]).strip("']"))
        #print (oid)
        #print("-社區:"+ varCommunity +"\n-IP:" + IP +"\n-Port:"+ varPort +"\n-OID:"+ oid )
        get_OID()
        
def get_OID():
    #############
    #SNMP取得OID#
    #############
    global o,oidValue
    for (errorIndication,errorStatus,errorIndex,varBinds) in getCmd(SnmpEngine(),
        CommunityData(varCommunity, mpModel=0),UdpTransportTarget((IP, varPort)),
        ContextData(),ObjectType(ObjectIdentity(oid))):
        
        if errorIndication or errorStatus:
            print(errorIndication or errorStatus)
            break
        else:
            for varBind in varBinds:
                n=48
                #o='value:'+str(varBind)[45:n]
                #print(o)
                oidValue = (str(varBind).split("="))[1].strip(" ")
                #print(oidValue)
                if (sensor_name == "T-sensor"):
                    confirm_Value()
                Sendsheet()
                #print(' = '.join([x.prettyPrint() for x in varBind]))

###################################
#         開啟URL                  #
###################################
def open_URL():
    import webbrowser
    webbrowser.open('https://docs.google.com/spreadsheets/d/1FRnBU64pL3ybZKUgu3R7WoUrK4gNcVa9NLCUOFZS3c8/edit#gid=0')  # Go to example.com

def Sendsheet():
    ###################################
    #            程式宣告區             #
    ###################################
    global zbar                       #-------------------->About全域變數of完成進度7/17

    import gspread
    from oauth2client.service_account import ServiceAccountCredentials 
    import string as string
    import random
    from pprint import pprint

    ###################################
    #           獲取授權與連結           #
    ###################################
    scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope) #權限金鑰
    client = gspread.authorize(creds)           #使用金鑰
    #sheet = client.open("2020-ES-ITR/FAF/Borrow/IR").sheet1   #指定googlesheet
    sheet = client.open("SNMP Data").worksheet('oid')#指定googlesheet
    
    #############
    #上傳資料處理#
    #############
    title = "Community" , "IP" , "Port" , "oid" , "location" , "sensor_name", "感測數值(生成)", "取樣時間(生成)"  
    all_info = [varCommunity , IP , varPort , oid , location , sensor_name , oidValue , time_now ]
    print(all_info)
    #index = 1
    #sheet.insert_row(title, index)
    index = 2
    sheet.insert_row(all_info, index)   

def confirm_Value():#判斷數值處理(因為溫度數值產出的3位數)
    global oidValue
    oidValue = int(oidValue)/10
    
def bar100():                               #------------------->About全域變數of完成進度7/17
    import time
    import progressbar

    for i in progressbar.progressbar(range(zbar)):
        time.sleep(0.1)
    
def tick():
    global count,result,varCommunity,IP,varPort,oid
    reset()
    now()
    get_TXT()
    open_URL()
        
    
if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(tick, 'cron', hour='00-23',minute='00-59') #每小時的每分鐘取得時間
    
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C    '))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass