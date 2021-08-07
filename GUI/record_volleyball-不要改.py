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
    
def total_input():
    #global 先設值在 查一下
    #並且要每個def都使用
    
        
    global serve,toss,squat,situp,stick,time_choose1,time_choose2,time_type2,data_choose,end,file_name,when_month,when_year  
    timeset=set()
    total=dict()
    file = open("timestamp.txt", "r")
    for line in file.readlines():
        #base64_bytes = line.encode("ascii")
        #sample_string_bytes = base64.b64decode(base64_bytes)
        #sample_string = sample_string_bytes.decode("ascii")
        dataset = json.loads(line)
        if dataset["time"][0:4]  not in timeset:
            timeset.add(dataset["time"][0:4])
            total[dataset["time"][0:4]]=dict()
        #print(dataset['time'][0:int(end)])
        #print(total[dataset["time"][0:int(end)]]['toss'])
    file.close()
    text=''

    root1 = Tk()
    root1.title("record")
    root1.geometry('500x500')
    
    time_choose1=0
    time_choose2=0
    time_type2=0
    data_choose=1
    end=4
    file_name='timestamp.txt'
    when_month=1
    when_year=2021
    def update_date(i):
        global serve,toss,squat,situp,stick,time_choose1,time_choose2,time_type2,data_choose,end,file_name,when_month,when_year


        
        
        
        time_choose1=0
        time_choose2=0
        time_type2=0
        data_choose=1
        end=4
        file_name='timestamp.txt'
        when_month=1
        when_year=2021
        print(i)
        if values[i]==0:
            
            time_choose1=0
            print(time_choose1)
            end=4
            print(end)
            return end
        if values[i]==1:
            time_choose1=1
            end=7
            return end
        if values[i]==2:
            time_choose1=2
            #file_name='timestamp.txt'
            end=10
            return end
            
    def update_makeup(i):
        global serve,toss,squat,situp,stick,time_choose1,time_choose2,time_type2,data_choose,end,file_name,when_month,when_year

        print('update_makeup',i)
        if values_makeup[i]==0:
            
            data_choose=1
            file_name='timestamp_file_no_makeup.txt'
            print('file_name',file_name)
            return file_name
        if values_makeup[i]==1:
            print("v_s5")
            data_choose=0
            file_name='timestamp.txt'         
            return file_name
    texts_makeup = ['是', '否']
    label_makeup = Label(root1,text='是否要刪除沒運動的日子')
    label_makeup.pack()
    values_makeup = [0, 1]
    select_makeup = IntVar()
    select_makeup.set(1)
    widget_makeup = [None]*len(texts_makeup)
    for i, (t, v) in enumerate(zip(texts_makeup, values_makeup)):
        widget_makeup[i] = Radiobutton(root1,
            text=t, value=v, variable=select_makeup,
            command=lambda index=i: update_makeup(index))
        widget_makeup[i].pack()#side=tk.LEFT

    texts = ['年', '月', '日']
    label_date = Label(root1,text='時間格式')
    label_date.pack()
    values = [0, 1, 2]
    select = IntVar()
    select.set(0)
    widget = [None]*len(texts)
    for i, (t, v) in enumerate(zip(texts, values)):
        if i==0:
            widget[i] = Radiobutton(root1,
                text=t, value=v, variable=select,
                command=lambda index=i: [update_date(index),label_year_show(comboExample_year,label_year_Top),label_month_forget(comboExample,label_month_Top)])
        elif i==1:
            widget[i] = Radiobutton(root1,
                    text=t, value=v, variable=select,
                    command=lambda index=i: [update_date(index),label_year_show(comboExample_year,label_month_Top),label_month_show(comboExample,label_month_Top)])
       
        
        elif i==2:
            widget[i] = Radiobutton(root1,
                    text=t, value=v, variable=select,
                    command=lambda index=i: [update_date(index),label_year_forget(comboExample_year,label_year_Top),label_month_forget(comboExample,label_month_Top)])
        widget[i].pack()
        
    timeset=list(timeset)#sort 失敗
    strings = [str(integer) for integer in timeset]
    a_string = "".join(strings)
    an_integer = int(a_string)
    #timeset=sorted(an_integer)
    timeset.insert(0,"無")
    label_year_Top = ttk.Label(root1,
                                text = "選擇你想查詢的年份")
    label_year_Top.pack()
    
    comboExample_year = ttk.Combobox(root1, 
                                values=timeset)
    
    
    #print(dict(comboExample)) 
    comboExample_year.pack()
    comboExample_year.current(0)
    when_year=comboExample_year.get()
    print(when_year) 
        #print(comboExample.current(), comboExample.get())   
    
    
    label_month_Top = ttk.Label(root1,
                                    text = "Choose your  month")
    label_month_Top.pack()
    
    comboExample = ttk.Combobox(root1,
                                values=['無','一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月'])
     
    comboExample.pack()
    comboExample.current(0)
    when_month=int(comboExample.current())+1
    print(when_month)
    def label_year_show(widget,label):

        label.pack()
        widget.pack()
        
    
    def label_year_forget(widget,label):

        label.pack_forget()
        widget.pack_forget()
    def label_month_show(widget,label):
        label.pack()
        widget.pack()
    
    def label_month_forget(widget,label):
        label.pack_forget()
        widget.pack_forget()
    ###確定
    def sure():
        """点击退出按钮时调用这个函数"""
        global when_year,when_month,time_choose2,end
        if comboExample_year.current()==0 and comboExample.current()==0:
            
            time_choose2=0
            

        else:
            if comboExample_year.current()!=0:
                end=7
            if comboExample.current()!=0:
                
                end=10
            time_choose2=1
            when_year=int(comboExample_year.get())
            if comboExample.current()<10:
                    
                when_month='0'+str(comboExample.current())
            else:
                when_month=int(comboExample.current())
        #root1.quit()  # 结束主循环
        print("time_choose2=0.",time_choose2," ",comboExample_year.current()," ", comboExample.current(),' ',end)
        #root1.destroy()  # 销毁窗口
    def _quit():
        """点击退出按钮时调用这个函数"""
        root1.quit()  # 结束主循环
        root1.destroy()  # 销毁窗口
    
    # 创建一个按钮,并把上面那个函数绑定过来
    #button0 = tk.Button(master=root1, text="確定", , font=("Arial", 15), relief=FLAT, bg='#14A769', fg='white',command=[sure(),quit()])
    button0=Button(master=root1, text="  OK  ", font=("Arial", 15), bg='#14A769', fg='white',  command=lambda:[sure(),_quit()])#, command=lambda:[sure,_quit]
           

    # 按钮放在下边
    button0.pack(side=BOTTOM)
    if "idlelib" not in sys.modules:
      root1.mainloop()
    #root1.mainloop()
    
    

    
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
    
    
    print('search',when_year)

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
    root2.title("在tkinter中使用matplotlib")
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
    root3.title("在tkinter中使用matplotlib")
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