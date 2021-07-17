# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 00:01:57 2021

@author: User
"""
import time # 引入time
import math 
import json
import base64
import matplotlib.pylab as plt
import numpy as np
from datetime import datetime
# today timestamp
timeStr = time.ctime()
struct_time = time.localtime() 
timeString = time.strftime("%Y-%m-%d ", struct_time)
timeString=timeString+" 00:00:00"
struct_time_lastrecord = time.strptime(timeString, "%Y-%m-%d %H:%M:%S") # 轉成時間元組
time_stamp_today = int(time.mktime(struct_time_lastrecord)) # 轉成時間戳
print(time_stamp_today)

#how many day are empty
day_empty= open("timestamp.txt", "r")
lines=day_empty.readlines()
dataset = json.loads(lines[-1])
timeString=dataset['time'][0:10]+" 00:00:00"

struct_time_lastrecord = time.strptime(timeString, "%Y-%m-%d %H:%M:%S") # 轉成時間元組
time_stamp_lastrecord = int(time.mktime(struct_time_lastrecord)) # 轉成時間戳
print(time_stamp_lastrecord)
day=math.ceil((time_stamp_today-time_stamp_lastrecord)/86400)#how many day
day_empty.close()

#Make_up_time
Make_up_time = open("timestamp.txt", "a+")
data=dict()
action=dict()
for i in range(day-1):
    add_record=time_stamp_lastrecord+86400*(i+1)
    print(add_record)
    struct_time_add = time.localtime(add_record) # 轉成時間元組
    add_record = time.strftime("%Y-%m-%d %H:%M:%S", struct_time_add) # 轉成字串
    action={'toss':0,'serve':0}
    data['time']=add_record
    data['action']=action
    Make_up_time.write(str(json.dumps(data)+'\n'))              
Make_up_time.close()




