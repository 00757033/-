from PIL import Image,ImageTk
from threading import Timer
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Physical.GUI_st
import Movement.live_toss
import Movement.live_serve
import Record.record
import Highlight.gui_highlight
import Dive.gui_dive
import sys
import cv2
import os
from sys import platform, version_info
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
chkValue = 0
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
    records = 0
    if chkValue.get() : 
       #messagebox.showinfo("record ", "record the video")
       records = 1
    if it==1:
        print("toss")
        t = Timer(3.0, Movement.live_toss.dect_loop(records)) 
        t.start()
    elif it==2:
        print("left serve")
        t = Timer(3.0, Movement.live_serve.dect_loop(0,records)) 
        t.start()
    else:
        print("right serve")
        t = Timer(3.0, Movement.live_serve.dect_loop(1,records)) 
        t.start()

def Menu1():
    #twd()
    newWindow2 = tk.Toplevel(window)
    newWindow2.title('movement detection')
    #newWindow2.iconphoto("pic/ssa.xbm")
    #newWindow2.iconbitmap('pic/ssa.ico')
    volleyballimg = Image.open('pic/volleyball_pic.png')
    volleyballimg = volleyballimg.resize((50, 50))
    recordimg = Image.open('pic/record.png')
    recordimg = recordimg.resize((50, 50))
    global tkvolleyballimg
    tkvolleyballimg = ImageTk.PhotoImage(volleyballimg)

    global tkrecordimg
    tkrecordimg = ImageTk.PhotoImage(recordimg)
    
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
    
    
    label1 = tk.Label(newWindow2, image=tkvolleyballimg)
    label1.image = tkvolleyballimg
    label1.grid(column=0, row=0)
    lab =tk.Label(newWindow2, text='Volleyball basic skills',fg='#FF8000',font=("Times", 40))
    lab.grid(column=1, row=0)
     
    
    global chkValue
    chkValue = tk.IntVar()
    
    BtnServeL = tk.Button(newWindow2, text='Left overhand serve',activebackground='#9D9D9D',bg='#9999CC',image=tkserveimg,compound = tk.LEFT,font=("Times", 25),command=partial(time,2))
    BtnServeR = tk.Button(newWindow2, text='Right overhand serve',activebackground='#9D9D9D',bg='#6FB7B7',image=tkserveimg,compound = tk.LEFT,font=("Times", 25),command=partial(time,3))
    BtnToss = tk.Button(newWindow2, text='Toss',activebackground='#9D9D9D',bg='#AFAF61',image=tktossimg,compound = tk.LEFT,font=("Times", 25),command=partial(time,1))
    Quit = tk.Button(newWindow2,text = "Exit",activebackground='#9D9D9D',bg='#B87070',image=tkexitimg,compound = tk.LEFT,font=("Times", 25), command = partial(destory,newWindow2))
    chkExample = tk.Checkbutton(newWindow2, text='Record',compound = tk.LEFT,font=("Times", 25), variable=chkValue,onvalue=1,offvalue=0) 
    #if chkExample.
    BtnRecord = tk.Button(newWindow2,text = "Video list",activebackground='#9D9D9D',bg='#3cb371',image=tkrecordimg,compound = tk.LEFT,font=("Times", 25), command = Record.record.record)
    BtnServeL.grid(column=0, row=1, columnspan=3,sticky='nswe')
    BtnServeR.grid(column=0, row=2, columnspan=3,sticky='nswe')
    BtnToss.grid(column=0, row=3, columnspan=3,sticky='nswe')
    Quit.grid(column=0, row=4,sticky='nswe')
    chkExample.grid(column=1, row=4)
    BtnRecord.grid(column=2, row=4)

def dive() : 
    newWindow3 = tk.Toplevel(window)
    newWindow3.title('Reaction training')
    global current_value
    current_value = tk.IntVar(value=0)
    box = tk.Spinbox(newWindow3,from_ = 1, to  = 5,textvariable=current_value,font=("Times", 25))
    box.grid(column=0, row=0, columnspan=3,sticky='nswe')
    #print("1 ", current_value.current())
    Btnspeed=tk.Button(newWindow3, text='correct',activebackground='#9D9D9D',bg='#AFAF61',compound = tk.LEFT,font=("Times", 25),command=diveGUI)
    #print("2 ", current_value.get())
    Btnspeed.grid(column=1, row=1, sticky='nswe')

def diveGUI() :
     Dive.gui_dive.dive(current_value.get())      
def version (pythoncode) :
   print(pythoncode,type(pythoncode))
   if pythoncode=='MovementDetection' or pythoncode=='highlight':
      if version_info.minor != 5 : 
         window.destroy()
         os.system("sh test.sh")
      elif  pythoncode=='MovementDetection':
           Menu1()
      elif pythoncode=='highlight' :
           os.system(Highlight.gui_highlight.highlight())
   else : 
      if version_info.minor != 7 :
         window.destroy() 
         os.system("sh test.sh")
      elif  pythoncode=='dive':
           dive()
      elif  pythoncode=='PhysicalTraining':
           os.system(Physical.GUI_st.total_init())
      
window = tk.Tk()
window.title('Sports  Analysis')
#window.iconbitmap('ssa.ico')
#window.geometry('580x400')
lbl_1 =tk.Label(window, text='Sports Skeleton Analysis',fg='#D94600',font=("Times", 50))
lbl_1.grid(column=0, row=0,columnspan=2)
PostureComparison = tk.Button(window, text='Movement Detection',activebackground='#9D9D9D',bg='#C7C7E2',font=("Times", 35),command=partial(version,'MovementDetection'))
PostureComparison.grid(column=0, row=1,sticky='nswe')
immediate = tk.Button(window, text='Physical Training',heigh=2,activebackground='#9D9D9D',bg='#ceb195',font=("Times", 35),command=partial(version,'PhysicalTraining'))
immediate.grid(column=1, row=1,sticky='nswe')
game = tk.Button(window, text='Dive',activebackground='#9D9D9D',bg='#add8e6',font=("Times", 35),command=partial(version,'dive'))
game.grid(column=0, row=2,sticky='nswe')
highlight = tk.Button(window, text='Highlight',heigh=2,activebackground='#9D9D9D',bg='#e9967a',font=("Times", 35),command=partial(version,'highlight'))
highlight.grid(column=1, row=2,sticky='nswe')
window.mainloop()
