# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 21:07:30 2021

@author: User
"""
import time
import json
import ast
import base64
t = time.localtime()
time = time.strftime("%Y/%m/%d %H:%M:%S", t)
#time = '2021/07/14 09:45:00'
# opening a text file

file1 = open("file.txt", "a+")
#dictionary = ast.literal_eval(file1.read())
#print(dictionary)
data=dict()
action=dict()
action={'toss':16,'serve':22}
data['time']=time
data['action']=action
database = str(json.dumps(data))
sample_string_bytes = database.encode("ascii")
base64_bytes = base64.b64encode(sample_string_bytes)
base64_string = base64_bytes.decode("ascii")
file1.write(base64_string+'\n')

file1.close()


