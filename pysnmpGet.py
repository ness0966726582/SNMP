import os
from apscheduler.schedulers.blocking import BlockingScheduler
from pysnmp.hlapi import * 

#先取得SNMP必要資訊
varCommunity = "public"
IP= "10.30.14.21" 
varPort = 161
oid1 = "1.3.6.1.4.1.2254.2.41.3.2.1.2.2"
oid2 = "1.3.6.1.4.1.2254.2.41.3.2.1.3.2"
o=[]

#自訂-OID1
def oid_1():
    global o
    for (errorIndication,errorStatus,errorIndex,varBinds) in getCmd(SnmpEngine(),
        CommunityData(varCommunity, mpModel=0),UdpTransportTarget((IP, 161)),
        ContextData(),ObjectType(ObjectIdentity(oid1))):
        
        if errorIndication or errorStatus:
            print(errorIndication or errorStatus)
            break
        else:
            for varBind in varBinds:
                n=48
                o='temperature:'+str(varBind)[45:n]+'C'
                print(o)
                #print(' = '.join([x.prettyPrint() for x in varBind]))

#自訂-OID2
def oid_2():
    global o
    for (errorIndication,errorStatus,errorIndex,varBinds) in getCmd(SnmpEngine(),
        CommunityData(varCommunity, mpModel=0),UdpTransportTarget((IP, 161)),
        ContextData(),ObjectType(ObjectIdentity(oid2))):
        
        if errorIndication or errorStatus:
            print(errorIndication or errorStatus)
            break
        else:
            for varBind in varBinds:
                n=49
                o='humidity:'+str(varBind)[45:n]+'%'
                print(o)
                #print(' = '.join([x.prettyPrint() for x in varBind]))
#自訂-功能勾選         
def tick():
    oid_1()
    oid_2()
#自訂-定時啟動    
if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(tick, 'cron', hour='00-23',minute='00-59') #每小時的每分鐘取得時間
    
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C    '))
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
