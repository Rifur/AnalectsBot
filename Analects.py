#!/usr/bin/python
# -*- coding:utf-8 -*-
 
import re
import json
import urllib2
import anatext as Ana
import time
import datetime
import random
import password
from plurk_oauth.PlurkAPI import PlurkAPI
 
plurk = password.NewPlurkAPI()
password.GetAuthorization(plurk);
 
Resped = []
print '=== Initial ==='
data = plurk.callAPI('/APP/Timeline/getPlurks?limit=5&minimal_data=true')
msgs = data.get('plurks')
for msg in msgs:
        pid = msg.get('plurk_id')
        if pid in Resped:
            continue
        Resped.append(pid)
        print pid
print '=== Initial done ==='

while True:
    try:
        plurk.callAPI('/APP/Alerts/addAllAsFriends')
    except: 
        print '[error]' + str(datetime.datetime.now()) + ' addAllAsFriends'
        pass

    try:
        time.sleep(10)
        data = plurk.callAPI('/APP/Timeline/getPlurks?limit=5&minimal_data=true')
    except:
        print '[error] ' + str(datetime.datetime.now()) + ' Timeout.'
        continue
    
    msgs = data.get('plurks')
    if not msgs:
        print str(datetime.datetime.now()) + ' No new plurks.'
        continue

    for msg in msgs:
        pid = msg.get('plurk_id')
        if pid in Resped:
            continue
        Resped.append(pid)
        print pid

        print msg.get('qualifier')
        if msg.get('qualifier') == 'asks':
            content = msg.get('content')
            print type(content)
            if content.find(u"孔子") != -1:
                print 'OK.'
                random.seed('%s%f' % (content, time.time()))
                f = random.sample(Ana.FirstVol, 1)[0]
                s = random.sample(Ana.SecondVol, 1)[0]
                if type(f) != list:
                    f = [f]
                for i in f:
                    plurk.callAPI('/APP/Responses/responseAdd',
                                    {'plurk_id': pid,
                                    'content': i,
                                    'qualifier': ':' })
                if type(s) != list:
                    s = [s]
                for i in s:
                    plurk.callAPI('/APP/Responses/responseAdd',
                                    {'plurk_id': pid,
                                    'content': i,
                                    'qualifier': ':' })
        
