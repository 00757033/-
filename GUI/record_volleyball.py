# -*- coding: utf-8 -*-
"""

"""
"""
Created on Tue Aug  3 10:12:14 2021

@author: User

tkinter圖 matplotlib.pyplot在运行的时候，是需要在主线程(Main Thread)上运行的，然而，我在使用多线程的时候，将使用matplotlib.pyplot的函数用在了子线程里面
加這三行
import matplotlib 
matplotlib.use('Agg')
from matplotlib import pyplot as plt 
https://www.codenong.com/cs105734243/
"""
#此會在開chat就跑

try:
        import sys
        import time
        import json
        import base64
        import matplotlib 
        from matplotlib import pyplot as plt        
        plt.switch_backend('agg') 
        import nest_asyncio
        nest_asyncio . apply ( )
        from PIL import Image
        import cv2
        import os
        from tkinter import *
        import numpy as np
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
        from matplotlib.backend_bases import key_press_handler
        from matplotlib.figure import Figure
        #from tkinter import *
        import tkinter.ttk as ttk
        from threading import Thread
except OSError as e:
    print(e)
def total_start():
    
    #print("888",search)
    Thread(args=total_input()).start()
    
def total_draw(file_name,end,time_choose2,when_year,when_month):
    file_name=file_name
    end=end
    time_choose2=time_choose2
    when_year=when_year
    when_month=when_month
    print("end",end)
################################################draw plot#######################################################
################################################draw data########################################################
    search=[]
    search_name=[]  
    serve=[]
    toss=[]
    squat=[] 
    situp=[]
    stick=[]         


    
    #print(end)
    timeset=set()
    total=dict()
    file = open(file_name, "r")
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

    file.close()
    
    
    print('search year',when_year)

    time=[]
    time1=[]
    for i in total:
        
        print(time_choose2," ",end," ",i," ",str(when_year)+'-0'+str(when_month)," ",i[0:7])
        if time_choose2==1 and end==7:
            if str(i[0:4])==str(when_year):
                print("end=4",i[0:4])
                #np.insert(time,-1,i)
                time.append(i)
                toss.append(total[i]['toss'])
                serve.append(total[i]['serve'])
                squat.append(total[i]['squat'])
                situp.append(total[i]['situp'])
                stick.append(total[i]['stick'])
                print('toss',toss)
                print('serve',serve)
                print('stick',stick)
        if time_choose2==1 and end==10:
            if str(i[0:7])==str(when_year)+'-'+str(when_month):
                print("357",i)
                #np.insert(time,-1,i)
                time.append(i)
                toss.append(total[i]['toss'])
                serve.append(total[i]['serve'])
                squat.append(total[i]['squat'])
                situp.append(total[i]['situp'])
                stick.append(total[i]['stick'])
        elif time_choose2!=1:
            print("here",i)
            print('toss',toss)
            print('serve',serve)
            print('stick',stick)
            time.append(i)
            toss.append(total[i]['toss'])
            serve.append(total[i]['serve'])
            squat.append(total[i]['squat'])
            situp.append(total[i]['situp'])
            stick.append(total[i]['stick'])
    search.append(toss)
    search.append(serve)
    search.append(squat)
    search.append(situp)
    search.append(stick)
    search_name.append('toss')
    search_name.append('serve')
    search_name.append('squat')
    search_name.append('situp')
    search_name.append('stick')
    width=0.15 
    print('len(search)',len(search))
    print('len(time)',len(time))
    print('stick',stick)
    print('search',search)
    print('search_name',search_name)
    #time= list(map(int,time))
    print(time)
    for i in range(len(time)):
        time1.append(i+1)
    x1=[p for p in time1]
    x2=[p-width for p in time1]
    x3=[p+ width for p in time1]
    x4=[p -2* width for p in time1]
    x5=[p + 2*width for p in time1]
    color=['#E8837E','#EFB28C','#EED19C','#ACBA90','#749D9B']
    x=[x1,x2,x3,x4,x5]

    
    
    
    
    ##################################stary draw1#############################################################
    #tkinter
    root2 = Tk()  # 创建tkinter的主窗口
    root2.title("ssa-record")
    f = Figure(figsize=(5, 4), dpi=100)
    a = f.add_subplot(111)  # 添加子图:1行1列第1个
        
    print('x1',x1)
    print('x2',x2)
    for i in range(len(search)):
        print(x[i]," ",search[i]," ",str(search_name[i])," ",color[i])
        a.bar(x[i], search[i], label=str(search_name[i]),color=color[i], align = "edge", width = 0.15) #繪製長條圖
    a.set_title("Personal Training") # title
    a.set_ylabel("count") # y label
    a.set_xlabel("Day") # x label
    
    colors=dict()
    for i in range(len(search)):
        print(search_name[i])
        color_temp={str(search_name[i]):color[i]}
        colors.update(color_temp)        
    labels = list(colors.keys())

    a.legend(labels)
    a.set_xticks(time1)
    a.set_xticklabels(time)

    

    # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
    canvas = FigureCanvasTkAgg(f, master=root2)
    canvas.draw()  # 注意show方法已经过时了,这里改用draw
    canvas.get_tk_widget().pack(side=TOP,  # 上对齐
                                fill=BOTH,  # 填充方式
                                expand=YES)  # 随窗口大小调整而调整
    
    # matplotlib的导航工具栏显示上来(默认是不会显示它的)
    toolbar = NavigationToolbar2Tk(canvas, root2)
    toolbar.update()
    canvas._tkcanvas.pack(side=TOP,  # get_tk_widget()得到的就是_tkcanvas
                          fill=BOTH,
                          expand=YES)
    
    
    def on_key_event(event):
        """键盘事件处理"""
        print("你按了%s" % event.key)
        key_press_handler(event, canvas, toolbar)
    
    
    # 绑定上面定义的键盘事件处理函数
    canvas.mpl_connect('key_press_event', on_key_event)
    
    
    def _quit():
        """点击退出按钮时调用这个函数"""
        root2.quit()  # 结束主循环
        root2.destroy()  # 销毁窗口
    
    
    # 创建一个按钮,并把上面那个函数绑定过来
    button = Button(master=root2, text="退出", command=_quit)
    # 按钮放在下边
    button.pack(side=BOTTOM)
        # 主循环
    root2.mainloop()
    
#########################################draw2###########################################################    


    
    
    
        #tkinter
    root3 = Tk()  # 创建tkinter的主窗口
    root3.title("ssa_record2")
    fig = Figure(figsize=(10, 8), dpi=100)
    ax1 = fig.add_subplot(511)  # 添加子图:1行1列第1个
    ax2 = fig.add_subplot(512)  # 添加子图:1行1列第1个
    ax3 = fig.add_subplot(513)  # 添加子图:1行1列第1个
    ax4 = fig.add_subplot(514)  # 添加子图:1行1列第1个
    ax5 = fig.add_subplot(515)  # 添加子图:1行1列第1个
    #fig,ax=Figure.subplots(5,1,figsize=(10,8))
    ax1.bar(time, toss, label='toss',color='#E8837E')
    ax1.legend(["toss"])
    ax2.bar(time, serve, label='serve',color='#EFB28C')  #繪製長條圖
    ax2.legend(["serve"])
    ax3.bar(time, squat, label='squat',color='#EED19C')
    ax3.legend(["squat"])
    ax4.bar(time, situp, label='situp',color='#ACBA90')
    ax4.legend(["situp"])
    ax5.bar(time, stick, label='stick',color='#749D9B')
    ax5.legend(["stick"])
        # 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
    canvas = FigureCanvasTkAgg(fig, master=root3)
    canvas.draw()  # 注意show方法已经过时了,这里改用draw
    canvas.get_tk_widget().pack(side=TOP,  # 上对齐
                                fill=BOTH,  # 填充方式
                                expand=YES)  # 随窗口大小调整而调整
    
    # matplotlib的导航工具栏显示上来(默认是不会显示它的)
    toolbar = NavigationToolbar2Tk(canvas, root3)
    toolbar.update()
    canvas._tkcanvas.pack(side=TOP,  # get_tk_widget()得到的就是_tkcanvas
                          fill=BOTH,
                          expand=YES)
    def on_key_event(event):
        """键盘事件处理"""
        print("你按了%s" % event.key)
        key_press_handler(event, canvas, toolbar)
    
    
    # 绑定上面定义的键盘事件处理函数
    canvas.mpl_connect('key_press_event', on_key_event)
    

    def _quit():
            
        
        root3.quit()  # 结束主循环
        root3.destroy()  # 销毁窗口
       # 创建一个按钮,并把上面那个函数绑定过来
    button = Button(master=root3, text="退出", command=_quit)
    # 按钮放在下边
    button.pack(side=BOTTOM)
    root3.mainloop()