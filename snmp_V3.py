'''
功能一
從Data1.txt取得snmp資訊,文檔包含以下
社區 + IP + 埠號 + OID (直接在文字檔內新增利用Tab鍵分隔)

功能二
定時擷取文檔內的OID

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
    #取得每行文字檔資料#
    ###############
    with open('Data1.txt','r',encoding='utf-8') as f:
        for line in f:
            result.append(list(line.strip('\n').split(',')))
    #檢視取得的資料
    #print(result)

    ###################
    #data.txt內使用行數#
    ###################
    file_dirs = 'Data1.txt'
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
        oid = str((keep[3]).strip("']"))
        print (oid)
        #print("-社區:"+ varCommunity +"\n-IP:" + IP +"\n-Port:"+ varPort +"\n-OID:"+ oid )
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

def tick():
    global count,result,varCommunity,IP,varPort,oid
    reset()
    get_TXT()
    
    
if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(tick, 'cron', hour='00-23',minute='00-59') #每小時的每分鐘取得時間
    
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C    '))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
