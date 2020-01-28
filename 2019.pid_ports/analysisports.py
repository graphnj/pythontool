# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""





netstat='''tcp        0      0 0.0.0.0:50020           0.0.0.0:*               LISTEN      17548/java          
tcp        0      0 192.168.1.10:9000       0.0.0.0:*               LISTEN      17260/java          
tcp        0      0 192.168.1.10:9001       0.0.0.0:*               LISTEN      17957/java          
tcp        0      0 127.0.0.1:45615         0.0.0.0:*               LISTEN      17548/java          
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:50070           0.0.0.0:*               LISTEN      17260/java          
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:50010           0.0.0.0:*               LISTEN      17548/java          
tcp        0      0 0.0.0.0:50075           0.0.0.0:*               LISTEN      17548/java          
tcp        0      0 192.168.1.10:60888      192.168.1.10:9000       ESTABLISHED 17548/java          
tcp        0      0 192.168.1.10:22         192.168.1.13:55460      ESTABLISHED -                   
tcp        0      0 192.168.1.10:35312      192.168.1.10:9000       TIME_WAIT   -                   
tcp        0    320 192.168.1.10:22         192.168.1.13:58853      ESTABLISHED -                   
tcp        0      0 192.168.1.10:22         192.168.1.13:58138      ESTABLISHED -                   
tcp        0      0 192.168.1.10:9000       192.168.1.10:60888      ESTABLISHED 17260/java          
tcp        0      0 192.168.1.10:22         192.168.1.13:55528      ESTABLISHED -                   
tcp6       0      0 192.168.1.10:8032       :::*                    LISTEN      12205/java          
tcp6       0      0 192.168.1.10:8033       :::*                    LISTEN      12205/java          
tcp6       0      0 192.168.1.10:41123      :::*                    LISTEN      30405/java          
tcp6       0      0 :::39461                :::*                    LISTEN      12920/java          
tcp6       0      0 :::4040                 :::*                    LISTEN      30405/java          
tcp6       0      0 :::8040                 :::*                    LISTEN      12920/java          
tcp6       0      0 :::7337                 :::*                    LISTEN      12920/java          
tcp6       0      0 :::8042                 :::*                    LISTEN      12920/java          
tcp6       0      0 127.0.0.1:36747         :::*                    LISTEN      30904/java          
tcp6       0      0 192.168.1.10:35405      :::*                    LISTEN      30405/java          
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
tcp6       0      0 192.168.1.10:8088       :::*                    LISTEN      12205/java          
tcp6       0      0 127.0.0.1:46649         :::*                    LISTEN      30930/java          
tcp6       0      0 192.168.1.10:8030       :::*                    LISTEN      12205/java          
tcp6       0      0 192.168.1.10:8031       :::*                    LISTEN      12205/java          
tcp6       0      0 192.168.1.10:59290      192.168.1.10:8032       ESTABLISHED 30405/java          
tcp6       0      0 192.168.1.10:38234      192.168.1.10:41123      ESTABLISHED 30904/java          
tcp6       0      0 192.168.1.10:41123      192.168.1.10:38224      ESTABLISHED 30405/java          
tcp6       0      0 192.168.1.10:44994      192.168.1.10:8031       ESTABLISHED 12920/java          
tcp6       0      0 192.168.1.10:38224      192.168.1.10:41123      ESTABLISHED 30778/java          
tcp6       0      0 192.168.1.10:8030       192.168.1.10:39396      ESTABLISHED 12205/java          
tcp6       0      0 192.168.1.10:41123      192.168.1.10:38238      ESTABLISHED 30405/java          
tcp6       0      0 192.168.1.10:41123      192.168.1.10:38234      ESTABLISHED 30405/java          
tcp6       0      0 192.168.1.10:8032       192.168.1.10:59290      ESTABLISHED 12205/java          
tcp6       0      0 192.168.1.10:38238      192.168.1.10:41123      ESTABLISHED 30930/java          
tcp6       0      0 192.168.1.10:8031       192.168.1.10:44994      ESTABLISHED 12205/java          
tcp6       0      0 192.168.1.10:39396      192.168.1.10:8030       ESTABLISHED 30778/java '''

jps='''30930 CoarseGrainedExecutorBackend
31973 Jps
30405 SparkSubmit
17957 SecondaryNameNode
12920 NodeManager
30904 CoarseGrainedExecutorBackend
30778 ExecutorLauncher
17548 DataNode
17260 NameNode
12205 ResourceManager'''

netstat=open("netstat.txt").read()
jps=open("jps.txt").read()

map_pidname={}
map_pidport={}
map_portpid={}
map_portremoteport=set()
nt=netstat.split('\n')
jpsline=jps.split('\n')
for j in jpsline:
    kv=j.split()
    map_pidname[kv[0]]=kv[1]
print(map_pidname)
for x in nt:
    v=x.split()
    localipport=v[3].split(':')
    remoteipport=v[4].split(':')
    localpidwithname=v[6].split('/')
    localpid=localpidwithname[0]
    if len(localpidwithname)==1:
        map_pidname[localpid]='system' 
    elif localpidwithname[1]!='java' and not map_pidname.get(localpidwithname[0]):
        map_pidname[localpid]=localpidwithname[1]
    print('-----------------------------\n'+localipport[1]+'  '+remoteipport[1]+'   '+localpid)

    oldset=(set() if None ==map_pidport.get(localpid) else map_pidport.get(localpid))
    print('oldset:',oldset,localipport[-1],oldset.add(localipport[-1]))
    map_pidport[localpid]=oldset
    print(map_pidport,oldset)
    map_portpid[localipport[-1]]=localpid
    map_portremoteport.add((localipport[-1],remoteipport[-1]))


for pid in map_pidport:
    strval=''
    for x in map_pidport[pid]:
        for y in map_portremoteport:
            #print(x,'y=',y,x==y[0])
            if y[0]==x:
                pname=map_pidname[map_portpid[y[1]]] if map_portpid.get(y[1]) else '*'
                strval+=x+'<-->'+pname+':'+y[1]+';'
    pidname=map_pidname[pid] if map_pidname.get(pid) else '-'
    print(pidname+'@'+pid+': '+strval)