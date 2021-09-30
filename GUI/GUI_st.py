# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 16:43:09 2021

@author: User
"""
try:
        import sys
        import time
        import json
        import base64
        import matplotlib 
        from matplotlib import pyplot as plt   
        import PIL.Image
        plt.switch_backend('agg') 

        from PIL import ImageTk, Image
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
        import record_volleyball
        import angle
except OSError as e:
    print(e)    
    



        

#if __name__=='__main__': #使用者輸入介面設定
def total_init():
    def total_input(forget):

    
        if forget==0:
            label_angle.pack_forget()
            widget_angle[0].pack_forget()
            widget_angle[1].pack_forget()
            widget_angle[2].pack_forget()
            widget_angle[3].pack_forget()
            widget_angle[4].pack_forget()
            button_angle.pack_forget()
            #label_makeup.pack()
            #widget_makeup[0].pack()#side=tk.LEFT
            #widget_makeup[1].pack()#side=tk.LEFT
            
            label_date.pack()
            widget[0].pack()
            widget[1].pack()
            widget[2].pack()
            label_year_Top.pack()
            comboExample_year.pack()
            #label_month_Top.pack()
            #comboExample.pack()
            button0.pack(side=BOTTOM)
    
        else:
            label_angle.pack()
            widget_angle[0].pack()
            widget_angle[1].pack()
            widget_angle[2].pack()
            widget_angle[3].pack()
            widget_angle[4].pack()
            button_angle.pack(side=BOTTOM)
            #label_makeup.pack_forget()
            label_date.pack_forget()
            #widget_makeup[0].pack_forget()#side=tk.LEFT
            #widget_makeup[1].pack_forget()#side=tk.LEFT
            
            widget[0].pack_forget()
            widget[1].pack_forget()
            widget[2].pack_forget()
            
            label_year_Top.pack_forget()
            
            comboExample_year.pack_forget()
            
            label_month_Top.pack_forget()
            
            
            
            comboExample.pack_forget()
            
            button0.pack_forget()
    self_train = Toplevel() #創 tk inter的視窗
    style_choose = ttk.Style()
    style_choose.configure("BW.TLabel", background='#5F9EAD',foreground='Snow')
    
    self_train.title("SSA-Physical training")
    self_train.geometry('600x1000') #設定視窗大小
    #self_train.iconphoto(True, PhotoImage(file="ssa.png"))
    img=PIL.Image.open("ssa.png")
    img = img.resize((600, 200))
    img=ImageTk.PhotoImage(img)
    imLabel=Label(self_train,image=img)
    imLabel.pack()
    self_train_system = ttk.Label(self_train, text = "Choose the mode")
    self_train_system.pack() 
    self_train_system.configure(font=("Courier", 30, "italic"), style="BW.TLabel")
    texts = ['Physical Training Judgment', 'Physical Training Results ']
    values = [0, 1]
    select = IntVar()
    select.set(1)
    widget = [None]*len(texts)
    for i, (t, v) in enumerate(zip(texts, values)):
        print(i)
        if i==0 :
            widget[i] = Radiobutton(self_train,
                text=t, value=v, variable=select,
                command=lambda index=i: total_input(1))
    
        elif i==1  :
            widget[i] = Radiobutton(self_train,
                text=t, value=v, variable=select,
                command=lambda index=i: total_input(0))
    
        widget[i].pack()
        widget[i].configure(font=("Times", 20))
    #分割線
    s=ttk.Style()
    s.configure('TSeparator',background='#FDF5E6')
    b=ttk.Separator(self_train,orient='horizontal',
                    style='TSeparator')
    b.pack(fill=X)
    global serve,toss,squat,situp,stick,time_choose1,time_choose2,time_type2,data_choose,end,file_name,when_month,when_year,goaltime,action
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
    file.close()
    text=''   
    time_choose1=0
    time_choose2=0
    time_type2=0
    data_choose=1
    end=4
    file_name='timestamp.txt'
    when_month=1
    when_year=2021
    goaltime=0
    action='toss'
    def update_date(i):#年月日
        global time_choose1,end
        #print(i)
        if values[i]==0:
            
            time_choose1=0
            print('time_choose1',time_choose1)
            end=4
            print('end',end)
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
            
    def update_makeup(i):#是否去掉沒訓練的日子
        global data_choose,file_name
        if values_makeup[i]==0:
            data_choose=1
            file_name='timestamp_file_no_makeup.txt'
            print('file_name',file_name)
            return file_name
        if values_makeup[i]==1:
    
            data_choose=0
            file_name='timestamp.txt'      
            print('file_name',file_name)
            return file_name
    texts_makeup = ['是', '否']
    label_makeup = Label(self_train,text='是否要刪除沒運動的日子')
    
    #label_makeup.pack() 
    label_makeup.configure(font=("Times", 18))
    values_makeup = [0, 1]
    select_makeup = IntVar()
    select_makeup.set(1)
    widget_makeup = [None]*len(texts_makeup)
    for i, (t, v) in enumerate(zip(texts_makeup, values_makeup)):
        widget_makeup[i] = Radiobutton(self_train,
            text=t, value=v, variable=select_makeup,
            command=lambda index=i: update_makeup(index))
        #if i==0:
          #widget_makeup[i].grid(column=0, row=1, sticky='nwes')#side=tk.LEFT
          #widget_makeup[i].configure(font=("Times", 18))
        #else:
          #widget_makeup[i].pack(side='right')#side=tk.LEFT
          #widget_makeup[i].configure(font=("Times", 18))
    texts = ['year', 'month', 'day']
    label_date = Label(self_train,text='Time format')
    
    label_date.pack()
    label_date.configure(font=("Times", 18))
    values = [0, 1, 2]
    select = IntVar()
    select.set(0)
    widget = [None]*len(texts)
    for i, (t, v) in enumerate(zip(texts, values)):
        
        if i==0:
            widget[i] = Radiobutton(self_train,
                text=t, value=v, variable=select,
                command=lambda index=i: [update_date(index),label_year_show(comboExample_year,label_year_Top),label_month_forget(comboExample,label_month_Top)])
        elif i==1:
            widget[i] = Radiobutton(self_train,
                    text=t, value=v, variable=select,
                    command=lambda index=i: [update_date(index),label_year_show(comboExample_year,label_month_Top),label_month_show(comboExample,label_month_Top)])
       
        
        elif i==2:
            widget[i] = Radiobutton(self_train,
                    text=t, value=v, variable=select,
                    command=lambda index=i: [update_date(index),label_year_forget(comboExample_year,label_year_Top),label_month_forget(comboExample,label_month_Top)])
        
        widget[i].pack()
        widget[i].configure(font=("Times", 18))        
        
    timeset=list(timeset)
    strings = [str(integer) for integer in timeset]
    timeset=sorted(strings)
    print(timeset)
    timeset.insert(0,"no")
    label_year_Top = ttk.Label(self_train,
                                text = "Select the year you want to query")
    
    label_year_Top.pack()
    label_year_Top.configure(font=("Times", 20))    
    
    comboExample_year = ttk.Combobox(self_train, 
                                values=timeset)
    
    
    #print(dict(comboExample)) 
    
    comboExample_year.pack()
    comboExample_year.configure(font=("Times", 18))
    comboExample_year.current(0)
    when_year=comboExample_year.get()
    print('when_year',when_year) 
        #print(comboExample.current(), comboExample.get())   
    
    
    label_month_Top = ttk.Label(self_train,
                                    text = "Select the month you want to query")
    
    label_month_Top.pack_forget()
    label_month_Top.configure(font=("Times", 20))      
    
    comboExample = ttk.Combobox(self_train,
                                values=['no','Jan','Feb','Mar','Apr','May','Jun','JUl','Aug','Sep','Oct','Nov','Dec'])
    
    comboExample.pack_forget()
    comboExample.configure(font=("Times", 18))
    comboExample.current(0)
    when_month=int(comboExample.current())+1
    print('when_year',when_month)
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
    
        print("time_choose2=0.",time_choose2," ",comboExample_year.current()," ", comboExample.current(),' ',end)
    def _quit():
        """点击退出按钮时调用这个函数"""
        self_train.quit()  # 结束主循环
        self_train.destroy()  # 销毁窗口
    
    # 创建一个按钮,并把上面那个函数绑定过来
    button0=Button(master=self_train, text="  OK  ", font=("Arial", 20), bg='#14A769', fg='white',  command=lambda:[sure(),_quit(),record_volleyball.total_draw(file_name,end,time_choose2,when_year,when_month)])#, command=lambda:[sure,_quit]
           
    
    # 按钮放在下边
    
    button0.pack(side=BOTTOM)
    
    
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
    def _quit():
        """点击退出按钮时调用这个函数"""
        self_train.quit()  # 结束主循环
        self_train.destroy()  # 销毁窗口
    #################################################angle tkinter ###############################
    
    texts_angle = ['toss', 'serve', 'squat','situp','plank']
    texts_angle_name = ['toss', 'serve', 'squat','situp','stick']
    label_angle = Label(self_train,text='choose action to test')
    
    label_angle.pack_forget()
    label_angle.configure(font=("Times", 20))
    
    values_angle = [0, 1, 2,3,4]
    select_angle = IntVar()
    select_angle.set(0)
    widget_angle = [None]*len(texts_angle)
    for i, (t, v) in enumerate(zip(texts_angle, values_angle)):
    
        if i==0:
            print("i",i)
            widget_angle[i] = Radiobutton(self_train,
                text=t, value=v, variable=select_angle,command=lambda index=i:[hide_time(time_label,time_entry),show_action(texts_angle_name[index])])
        elif i==1:
            widget_angle[i] = Radiobutton(self_train,
                    text=t, value=v, variable=select_angle,command=lambda index=i:[hide_time(time_label,time_entry),show_action(texts_angle_name[index])])
                    
        
        elif i==2:
            widget_angle[i] = Radiobutton(self_train,
                    text=t, value=v, variable=select_angle,command=lambda index=i:[hide_time(time_label,time_entry),show_action(texts_angle_name[index])])
        elif i==3:
            widget_angle[i] = Radiobutton(self_train,
                    text=t, value=v, variable=select_angle,command=lambda index=i:[hide_time(time_label,time_entry),show_action(texts_angle_name[index])])
        elif i==4:
            widget_angle[i] = Radiobutton(self_train,
                    text=t, value=v, variable=select_angle,command=lambda index=i:[show_time(time_label,time_entry),show_action(texts_angle_name[index])])
        
        widget_angle[i].pack_forget()
        widget_angle[i].configure(font=("Times", 20))
    e=StringVar()
    time_label=Label(self_train,text='Please enter the time (in seconds)')
    time_label.configure(font=("Times", 18))
    time_label.pack_forget()
    time_entry=Entry(self_train,textvariable=e,bd=18)
    
    
    time_entry.pack_forget()
    
    
    def show_time(time_label,time_entry):

        time_label.pack()
        time_entry.pack()
    def hide_time(time_label,time_entry):
        global goaltime
        goaltime=0
        time_label.pack_forget()
        time_entry.pack_forget()
        return goaltime
    def _quit_angle():
        global goaltime
        goaltime=time_entry.get()
        print(":)",goaltime)
        """点击退出按钮时调用这个函数"""
        self_train.quit()  # 结束主循环
        self_train.destroy()  # 销毁窗口
        return goaltime
    def show_action(temp):
        print('temp',temp)
        global action
        action=temp
        return action

    button_angle=Button(master=self_train, text="  OK  ", font=("Arial", 15), bg='#14A769', fg='white',  command=lambda:[_quit_angle(),angle.training(action,goaltime)])#
    button_angle.pack_forget()
    if "idlelib" not in sys.modules:
      self_train.mainloop()
