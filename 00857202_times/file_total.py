
import time
import json
import base64
import matplotlib.pylab as plt
import numpy as np
t = time.localtime()
todaytime = time.strftime("%Y/%m/%d", t)
totaltoss = 0
totalserve = 0
timeset=set()
total=dict()
file2 = open("timestamp.txt", "r")
for line in file2.readlines():
    #base64_bytes = line.encode("ascii")
    #sample_string_bytes = base64.b64decode(base64_bytes)
    #sample_string = sample_string_bytes.decode("ascii")
    dataset = json.loads(line)
    if dataset["time"][0:10]  not in timeset:
        timeset.add(dataset["time"][0:10])
        total[dataset["time"][0:10]]=dict()
        total[dataset["time"][0:10]]['toss'] = 0
        total[dataset["time"][0:10]]['serve'] = 0
    total[dataset["time"][0:10]]['toss']+=dataset["action"]['toss']
    total[dataset["time"][0:10]]['serve']+=dataset["action"]['serve']
    print(dataset['time'])
file2.close()

#print(data)
#dataset = json.loads(data)
#print(dataset)
time=[]
serve=[]
toss=[]
for i in total:
    time.append(i)
    toss.append(total[i]['toss'])
    serve.append(total[i]['serve'])

plt.plot(time[::-1],toss[::-1],color=(201/255,109/255,81/255),label="toss")
plt.plot(time[::-1],serve[::-1],color=(70/255,140/255,156/255),label="serve")
plt.title("Personal Training") # title
plt.ylabel("count") # y label
plt.xlabel("Day") # x label
plt.legend()
plt.show()
titlename=['time','toss','serve']
a=np.asarray([time[::-1],toss[::-1],serve[::-1]])
a=a.T
a=np.insert(a,0,titlename,0)#numpy.insert(arr,obj,value,axis=None)
# save
np.savetxt("volleycsv.csv",a,fmt='%s',delimiter=',')
# read

 # opening a text file
