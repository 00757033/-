# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 00:14:57 2021

@author: User
"""
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 21:07:30 2021

@author: User
"""
import time
import json
import ast
t = time.localtime()
time = time.strftime("%Y-%m-%d %H:%M:%S", t)
#time = '2021/07/14 09:45:00'
# opening a text file

file1 = open("timestamp.txt", "a+")
#dictionary = ast.literal_eval(file1.read())
#print(dictionary)
data=dict()
action=dict()
action={'toss':16,'serve':22}
data['time']=time
data['action']=action
file1.seek(0, 0)
database = str(json.dumps(data))
file1.write(database+'\n')

file1.close()


