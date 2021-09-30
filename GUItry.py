from PIL import Image,ImageTk
from threading import Timer
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import GUI_st
import live_toss
import live_serve
import sys
import cv2
import os
from sys import platform
import argparse
import time
import numpy as np
import re
from functools import partial
video_name = 'video_'
file_type = '.avi'
_CAMERA_WIDTH = 640
_CAMERA_HEIGH = 480
prwrite_flag = 0
video_counter = 0
fourcc = cv2.VideoWriter_fourcc(*'XVID')
FPS = 20
#ShowMessage =tk.Text() 
def destory(Window):
    Window.destroy()
    home()
def twd():
    window.withdraw()
def home():
    window.wm_deiconify()
def clearToTextInput():
    ShowMessage.delete("1.0","end")
def Start():
    clearToTextInput()#-- 清空存放操作記錄的棧
    global write_flag
    write_flag = 1
    ShowMessage.insert('end', 'Start recording\n')
        
def End():
    global write_flag
    write_flag = 0
    ShowMessage.insert('end', 'End recording\n')
       
def OpenFile():
    name = tk.filedialog.askopenfilename()
    print(name)
    cap = cv2.VideoCapture(name)
    # Check if camera opened successfully
    if (cap.isOpened()== False): 
      print("Error opening video  file")  
    # Read until video is completed
    while(cap.isOpened()):     
      # Capture frame-by-frame
      ret, frame = cap.read()
      if ret == True:
        # Display the resulting frame
        cv2.imshow('Frame', frame)
        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
          break
      # Break the loop
      else: 
        break
       
    # When everything done, release 
    # the video capture object
    cap.release()
   
    # Closes all the frames
    cv2.destroyAllWindows() 
def time(it):
    #messagebox.showinfo("Time reminder", "Countdown to three seconds")
    if it==1:
        print("toss")
        t = Timer(3.0, live_toss.dect_loop) 
        t.start()
    elif it==2:
        print("serve")
        t = Timer(3.0, live_serve.dect_loop(1)) 
        t.start()
    else:
        print("serve")
        t = Timer(3.0, live_serve.dect_loop(0)) 
        t.start()
def Menu1():
    twd()
    newWindow2 = tk.Toplevel(window)
    newWindow2.title('movement detection')
    #newWindow2.iconphoto("pic/ssa.xbm")
    #newWindow2.iconbitmap('pic/ssa.ico')
    volleybalimg = Image.open('pic/volleyball_pic.png')
    volleybalimg = volleybalimg.resize((75, 75))
    global tkvolleybalimg
    tkvolleybalimg = ImageTk.PhotoImage(volleybalimg)
    
    tossimg = Image.open('pic/toss_pic.png')
    tossimg = tossimg.resize((50, 50))
    global tktossimg
    tktossimg = ImageTk.PhotoImage(tossimg)
    
    serveimg = Image.open('pic/serve_pic1.png')
    serveimg = serveimg.resize((50, 50))
    global tkserveimg
    tkserveimg = ImageTk.PhotoImage(serveimg)
    
    exitimg = Image.open('pic/exit.png')
    exitimg = exitimg.resize((50, 50))
    global tkexitimg
    tkexitimg = ImageTk.PhotoImage(exitimg)
    
    
    label1 = tk.Label(newWindow2, image=tkvolleybalimg)
    label1.image = tkvolleybalimg
    label1.grid(column=0, row=0)
    lab =tk.Label(newWindow2, text='Volleyball basic skills',fg='#FF8000',font=("Times", 40))
    lab.grid(column=1, row=0)
    BtnServeL = tk.Button(newWindow2, text='Left overhand serve',activebackground='#9D9D9D',bg='#9999CC',image=tkserveimg,compound = tk.LEFT,font=("Times", 25),command=partial(time,2))
    BtnServeR = tk.Button(newWindow2, text='Right overhand serve',activebackground='#9D9D9D',bg='#6FB7B7',image=tkserveimg,compound = tk.LEFT,font=("Times", 25),command=partial(time,3))
    BtnToss = tk.Button(newWindow2, text='Toss',activebackground='#9D9D9D',bg='#AFAF61',image=tktossimg,compound = tk.LEFT,font=("Times", 25),command=partial(time,1))
    Quit = tk.Button(newWindow2,text = "Exit",activebackground='#9D9D9D',bg='#B87070',image=tkexitimg,compound = tk.LEFT,font=("Times", 25), command = partial(destory,newWindow2))
    Quit.grid(column=0, row=4,sticky='nswe')
    BtnServeL.grid(column=0, row=1, columnspan=2,sticky='nswe')
    BtnServeR.grid(column=0, row=2, columnspan=2,sticky='nswe')
    BtnToss.grid(column=0, row=3, columnspan=2,sticky='nswe')

        

        

window = tk.Tk()
window.title('Sports  Analysis')
#window.iconbitmap('ssa.ico')
#window.geometry('580x400')
lbl_1 =tk.Label(window, text='Sports Skeleton Analysis',fg='#D94600',font=("Times", 50))
lbl_1.grid(column=0, row=0,columnspan=2)
PostureComparison = tk.Button(window, text='Movement detection',activebackground='#9D9D9D',bg='#C7C7E2',font=("Times", 35),command=Menu1)
PostureComparison.grid(column=0, row=1,sticky='nswe')
immediate = tk.Button(window, text='Physical Training',heigh=2,activebackground='#9D9D9D',bg='#ceb195',font=("Times", 35),command=GUI_st.total_init)
immediate.grid(column=1, row=1,sticky='nswe')
window.mainloop()
