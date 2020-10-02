'''
get_TXT()抓取文字檔內容,包含以下
-將獲取的重要資訊宣告為全域變數
-開啟Data.txt (utf-8)
-計算Data.txt使用行數切割做陣列
-取用字串的處理
-印出Data.txt內的OID再引用 "get_OID()"

get_OID()SNMP抓取線上的OID,包含以下
-產出OID數值

定時擷取
'''


import os
from apscheduler.schedulers.blocking import BlockingScheduler
from pysnmp.hlapi import * 
                
import sys
count = 0    #計數變量
result = []
varCommunity = ""
IP = ""
varPort = ""
oid = ""

def get_TXT():
    global count,result,varCommunity,IP,varPort,oid
    ###############
    #取得文字檔資料#
    ###############
    with open('Data.txt','r',encoding='utf-8') as f:
        for line in f:
            result.append(list(line.strip('\n').split(',')))
    #檢視取得的資料
#   print(result)

    ###################
    #data.txt內使用行數#
    ###################
    file_dirs = 'Data.txt'
    filename = open(file_dirs,'r',encoding='utf-8')        #以只读方式打开文件
    file_contents = filename.read()       #读取文档内容到file_contents
    for file_content in file_contents:    #统计文件内容中换行符的数目
        if file_content == '\n':
            count += 1
    if file_contents[-1] != '\n':         #当文件最后一个字符不为换行符时，行数+1
        count += 1
#    print('文件%s總共有%d行' % (file_dirs, count))

    #########
    #資料處理#
    #########
    varCommunity = (str(result[0])[18:24])
    IP = (str(result[1])[7:18])
    varPort = (str(result[2])[12:15])
#   print("固定資料\n-使用區:"+ varCommunity +"\n-IP:" + IP +"\n-選用阜:"+ varPort )

    ################
    #印出目前有的OID#
    ################
    for i in range(4,count):
        i+1
        #print("第", i+1, "行OID為",(str(result[i])[2:35]))
        oid = str(result[i])[3:34]
        print(oid)
        get_OID()
        
def get_OID():
    #############
    #SNMP取得OID#
    #############
    global o
    for (errorIndication,errorStatus,errorIndex,varBinds) in getCmd(SnmpEngine(),
        CommunityData(varCommunity, mpModel=0),UdpTransportTarget((IP, varPort)),
        ContextData(),ObjectType(ObjectIdentity(oid))):
        
        if errorIndication or errorStatus:
            print(errorIndication or errorStatus)
            break
        else:
            for varBind in varBinds:
                n=48
                o='value:'+str(varBind)[45:n]
                print(o)
                #print(' = '.join([x.prettyPrint() for x in varBind]))
def reset():
    ########
    #全歸零#
    ########
    count = 0    
    result = []
    varCommunity = ""
    IP = ""
    varPort = ""
    oid = ""



def tick():
    global count,result,varCommunity,IP,varPort,oid
    get_TXT()
    print(str(varCommunity) +"\n" + str(IP) +"\n" + str(varPort))
    reset()
    
if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(tick, 'cron', hour='00-23',minute='00-59') #每小時的每分鐘取得時間
    
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C    '))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
