from PIL import Image,ImageTk
from threading import Timer
import tkinter as tk
from tkinter import Tk, Menu, filedialog
import cv2
video_name = 'video_'
file_type = '.avi'
_CAMERA_WIDTH = 640
_CAMERA_HEIGH = 480
prwrite_flag = 0
video_counter = 0
fourcc = cv2.VideoWriter_fourcc(*'XVID')
FPS = 20
#ShowMessage =tk.Text() 
def clearToTextInput():
    ShowMessage.delete("1.0","end")
def Start():
    clearToTextInput()#-- 清空存放操作記錄的棧
    global write_flag
    write_flag = 1
    ShowMessage.insert('end', '開始錄影\n')
        
def End():
    global write_flag
    write_flag = 0
    ShowMessage.insert('end', '結束錄影\n')
       
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
def time():
    #newWindow3 = tk.Toplevel(window)
    #label = tk.Label(newWindow3,font=("Times", 30), text= '倒數5秒')
    #label.grid(column=0, row=0)
    t = Timer(5.0, dect_loop()) 
    t.start()
def Menu1():
    newWindow2 = tk.Toplevel(window)
    newWindow2.title('姿勢')
    #newWindow2.geometry('800x750')
    lab =tk.Label(newWindow2, text='排球姿勢檢測',font=("Times", 30))
    lab.grid(column=0, row=0)
    BtnServeL = tk.Button(newWindow2, text='左手上手發球',width=20,font=("Times", 20),command=time)
    BtnServeR = tk.Button(newWindow2, text='右手上手發球',width=20,font=("Times", 20),command=time)
    BtnToss = tk.Button(newWindow2, text='托球',width=20,font=("Times", 20),command=time)
    BtnServeL.grid(column=0, row=1, sticky='nwes')
    BtnServeR.grid(column=0, row=2, sticky='nwes')
    BtnToss.grid(column=0, row=3, sticky='nwes')

    #download = tk.Button(newWindow2, text=' 影片上傳 ',width=30,height=5,font=("Times", 20),command=OpenFile)
    #download.grid(column=0, row=3)
    #StartRecord = tk.Button(newWindow2, text=' 開始錄影 ',width=10, command=Start)
    #StartRecord.grid(column=2, row=1)
    #EndRecord = tk.Button(newWindow2, text=' 結束錄影 ',width=10, command=End)
    #EndRecord.grid(column=2, row=2)
    #scrollbar = tk.Scrollbar(newWindow)
    #scrollbar.place(x=1050,y=100)
    #global ShowMessage
    #ShowMessage = tk.Text(newWindow2,width=33, height=25, background = "black",foreground="white")
    '''
    for i in range(40):
         #插入內容到 listbox 尾端
         ShowMessage.insert('end', str(i)+"\n")
    # side='left' 放入左邊
    # fill='both' 向 x 軸和 y 軸填滿
    # expand=1 開啟 fill
    '''
    #ShowMessage.grid(column=1, row=0, rowspan=4)
    # scrollbar 移動時使 listbox 跟著移動
    
    #scrollbar.config(command=ShowMessage.yview)
def Menu2():
    newWindow = tk.Toplevel()
    #newWindow.geometry('1000x800')
    panel = tk.Label(newWindow)  # initialize image panel
    panel.place(x=0,y=0)

    download = tk.Button(newWindow, text=' 影片上傳 ',width=10,command=OpenFile)
    download.place(x=150,y=10)
    #StartRecord = tk.Button(newWindow, text=' 開始錄影 ',width=10, command=Start)
    #StartRecord.place(x=750,y=10)
    #EndRecord = tk.Button(newWindow, text=' 結束錄影 ',width=10, command=End)
    #EndRecord.place(x=850,y=10)
    #scrollbar = tk.Scrollbar(newWindow)
    #scrollbar.place(x=1050,y=100)
    #global ShowMessage
    #ShowMessage = tk.Text(newWindow,width=33, height=25, background = "black",foreground="white")
    '''
    for i in range(40):
         #插入內容到 listbox 尾端
         ShowMessage.insert('end', str(i)+"\n")
    # side='left' 放入左邊
    # fill='both' 向 x 軸和 y 軸填滿
    # expand=1 開啟 fill
    '''
    #ShowMessage.place(x=650,y=50)
    # scrollbar 移動時使 listbox 跟著移動
    
    #scrollbar.config(command=ShowMessage.yview)
    #dect_loop()
        
def dect_loop():
    cnt=0
    global video_counter
    write_flag = 0 
    cap = cv2.VideoCapture(0)# 設定擷取影像的尺寸大小
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, _CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, _CAMERA_HEIGH)
    while(cap.isOpened()):
        cnt+=1
        if cnt==100:
            break
        ret, frame = cap.read()
        if ret == True:
            if cv2.waitKey(10) & 0xFF == ord('r') and write_flag == 0: # 寫入影格
                write_flag = 1
                save_name = video_name + str(video_counter) + file_type
                global out2
                out2 = cv2.VideoWriter(save_name, fourcc, FPS, (_CAMERA_WIDTH, _CAMERA_HEIGH))
                print('writing to ' + save_name)
            elif cv2.waitKey(10) & 0xFF == ord('t') and write_flag == 1: #關閉影片
                write_flag = 0
                video_counter = video_counter + 1
                print('finish')
            elif cv2.waitKey(10) & 0xFF == ord('s'): # 釋放所有資源
                cap.release()
                out2.release()
                cv2.destroyAllWindows()
                break
    
            if (write_flag == 1):
                out2.write(frame)    
            cv2.imshow('frame',frame)
        else:
            break
    cv2.destroyAllWindows()          

window = tk.Tk()
window.title('window')
#window.geometry('580x400')
lbl_1 =tk.Label(window, text='運動分析',font=("Times", 40))
lbl_1.grid(column=0, row=0,columnspan=3)
PostureComparison = tk.Button(window, text='姿勢比對',width=10,height=3,font=("Times", 30),command=Menu1)
PostureComparison.grid(column=1, row=1)
immediate = tk.Button(window, text='自我練習',width=10,height=3,font=("Times", 30),command=Menu1)
immediate.grid(column=2, row=1)
window.mainloop()
