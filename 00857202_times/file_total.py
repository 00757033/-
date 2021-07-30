
#year 0:4
#month 0:7
#day 0:10
import time
import json
import base64
import matplotlib.pylab as plt

import numpy as np



serve=[]
toss=[]
squat=[]
situp=[]
stick=[]
time_type1=""
time_type2=""
action=""
data_type=""
end=0
time_choose1=5
time_choose2=5
action_choose3=5
data_choose=1
search=[]
search1='有'
while (1):
    action=input("請輸入動作action:toss serve 深蹲 仰臥起坐 棒式 全部")
    print(action)
    if action=="toss" and search1=='有':
        action_choose3=0
        search.append(toss)
        search1=input("還有嗎?(有/沒有)")
    if action=="serve"and search1=='有':
        print(search1)
        action_choose3=1
        search.append(serve)
        search1=input("還有嗎?(有/沒有)")
        #break
    if action=="深蹲"and search1=='有':
        action_choose3=2
        search.append(squat)
        search1=input("還有嗎?(有/沒有)")
        #break
    if action=="仰臥起坐"and search1=='有':
        action_choose3=3
        search.append(situp)
        search1=input("還有嗎?(有/沒有)")
        #break
    if action=="棒式"and search1=='有':
        action_choose3=4
        search.append(stick)
        search1=input("還有嗎?(有/沒有)")
        #break
    if action=="全部"and search1=='有':
        action_choose3=5
        search.append(action)
        search1=input("還有嗎?")
        #break
    if search1=="沒有":
        print(search1)
        break
while (1):
    
    time_type1=input("請輸入想查詢的格式時間太長不建議天數( 年/月/日)")
    print(time_type1)
    if time_type1== "年" :
        time_choose1=0
        end=4
    if time_type1== "月" :
        time_choose1=1
        end=7
    if time_type1=="日" :
        #print(time_type1)
        time_choose1=2
        end=10
    if time_choose1==0 or time_choose1==1 or time_choose1==2 :
        print(time_choose1)
        break
while (1):
    time_type2=input("是否特定查詢 yes/no")
    
    if time_type2=="是" :
        time_choose2=1
        print(time_type2)
        
            
    elif time_type2=="否" :
        time_choose2=0
    else:
        time_choose2=3
    if time_choose2==1 or time_choose2==0:
            break
while (1):
    data_type=input("是否要去除沒訓練的天數")
    
    if data_type=="是" :
        data_choose=1
        print(time_type2)
        
            
    elif data_type=="否" :
        data_choose=0
    else:
        data_choose=3
    if data_choose==1 or data_choose==0:
            break            

    





t = time.localtime()
todaytime = time.strftime("%Y/%m/%d", t)
totaltoss = 0
totalserve = 0

timeset=set()
total=dict()
file = open("timestamp.txt", "r")
for line in file.readlines():
    #base64_bytes = line.encode("ascii")
    #sample_string_bytes = base64.b64decode(base64_bytes)
    #sample_string = sample_string_bytes.decode("ascii")
    dataset = json.loads(line)
    if dataset["time"][0:int(end)]  not in timeset:
        timeset.add(dataset["time"][0:int(end)])
        total[dataset["time"][0:int(end)]]=dict()
        total[dataset["time"][0:int(end)]]['toss'] = 0
        total[dataset["time"][0:int(end)]]['serve'] = 0
        total[dataset["time"][0:int(end)]]['squat'] = 0
        total[dataset["time"][0:int(end)]]['situp'] = 0
        total[dataset["time"][0:int(end)]]['stick'] = 0
    total[dataset["time"][0:int(end)]]['toss']+=dataset["action"]['toss']
    total[dataset["time"][0:int(end)]]['serve']+=dataset["action"]['serve']
    total[dataset["time"][0:int(end)]]['squat']+=dataset["action"]['squat']
    total[dataset["time"][0:int(end)]]['situp']+=dataset["action"]['situp']
    total[dataset["time"][0:int(end)]]['stick']+=dataset["action"]['stick']
    
    #print(dataset['time'][0:int(end)])
    #print(total[dataset["time"][0:int(end)]]['toss'])
file.close()

#print(data)
#dataset = json.loads(data)
#print(dataset)
time=[]
time1=[]

for i in total:
    print(i)
    #np.insert(time,-1,i)
    time.append(i)
    toss.append(total[i]['toss'])
    serve.append(total[i]['serve'])
    squat.append(total[i]['squat'])
    situp.append(total[i]['situp'])
    stick.append(total[i]['stick'])
width=0.15 
print(len(time))
print(stick)
print(toss)
#time= list(map(int,time))
print(time)
for i in range(len(time)):
    time1.append(i+1)
x1=[p- 2*width for p in time1]
x2=[p-width for p in time1]
x3=[p for p in time1]
x4=[p+ width for p in time1]
x5=[p + 2*width for p in time1]
color=['#E8837E','#EFB28C','#EED19C','#ACBA90','#749D9B']
x=[x1,x2,x3,x4,x5]
plt.figure(0)

for i in range(len(search)):
    print(x[i]," ",search[i]," ",str(search[i])," ",color[i])
    plt.bar(x[i], search[i], label=str(search[i]),color=color[i], align = "edge", width = 0.15) #繪製長條圖
#plt.bar(x1, serve, label='serve',color='#EFB28C', align = "edge", width = 0.15)  #繪製長條圖
#plt.bar(x2, squat, label='squat',color='#EED19C', align = "edge", width = 0.15) #繪製長條圖
#plt.bar(x4, situp, label='situp',color='#ACBA90', align = "edge", width = 0.15)  #繪製長條圖plt.bar(time[::1], toss[::1], label='toss',color=(201/255,109/255,81/255), align = "edge", width = 0.25) #繪製長條圖
#plt.bar(x5, stick, label='stick',color='#749D9B', align = "edge", width = 0.15)  #繪製長條圖
#plt.xticks([p+width for p in time],time)
#plt.bar(time[::1],toss[::1],color=(201/255,109/255,81/255),label="toss")
#plt.bar(time[::1],serve[::1],color=(70/255,140/255,156/255),label="serve")
plt.title("Personal Training") # title
plt.ylabel("count") # y label
plt.xlabel("Day") # x label
colors = {'toss':'#FFC9DE', 'serve':'green','squat':'#FFC9DE', 'situp':'green','stick':'#FFC9DE'}         
labels = list(colors.keys())
plt.legend(labels)
plt.xticks([p+width for p in x1],time)

plt.show()
#end 多個表格

plt.figure(1)
fig,ax=plt.subplots(5,1,figsize=(10,8))
ax[0].bar(time, toss, label='toss',color='#E8837E')
ax[0].legend(["toss"])
ax[1].bar(time, serve, label='serve',color='#EFB28C')  #繪製長條圖
ax[1].legend(["serve"])
ax[2].bar(time, squat, label='squat',color='#EED19C')
ax[2].legend(["squat"])
ax[3].bar(time, situp, label='situp',color='#ACBA90')
ax[3].legend(["situp"])
ax[4].bar(time, stick, label='stick',color='#749D9B')
ax[4].legend(["stick"])
plt.show()

'''
titlename=['time','toss','serve','squat', 'situp','stick']
a=np.asarray([time,toss[::-1],serve[::-1],squat[::-1],situp[::-1],stick[::-1]])
a=a.T
a=np.insert(a,0,titlename,0)#numpy.insert(arr,obj,value,axis=None)
# save
np.savetxt("volleycsv.csv",a,fmt='%s',delimiter=',')
# read

 # opening a text file
'''
