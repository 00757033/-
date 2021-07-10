from PIL import Image,ImageTk

import tkinter as tk
from tkinter import Tk, Menu, filedialog
import cv2


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("排球")
        self.geometry('300x140')
        self.label = tk.Label(self, text='排球',font=("Times", 40))
        self.label.place(x=90,y=10)
        self.PostureComparison = tk.Button(self, text='姿勢比對',command=self.Menu1)
        self.PostureComparison.place(x=40,y=80)
        self.immediate = tk.Button(self, text='即時累計',command=self.Menu2)
        self.immediate.place(x=180,y=80)
        self.camera = cv2.VideoCapture(0)    #摄像头
        self.video_name = 'video_' #儲存影片名稱
        self.file_type = '.avi' #儲存影片副檔名
        self._CAMERA_WIDTH = 640  #攝影機擷取影像寬度
        self._CAMERA_HEIGH = 480  #攝影機擷取影像高度
        self.write_flag = 0  #判斷是否為寫入模式
        self.prwrite_flag = 0
        self.video_counter = 0  #計數儲存影片數量
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.FPS = 20  #擷取影片頻率
    def Menu1(self):
        self.newWindow2 = tk.Toplevel(self)
        self.newWindow2.geometry('1000x500')
        radioValue = tk.IntVar() 
        rdioOne = tk.Radiobutton(self.newWindow2, text='January',variable=radioValue, value=1) 
        rdioTwo = tk.Radiobutton(self.newWindow2, text='Febuary',variable=radioValue, value=2) 
        rdioThree = tk.Radiobutton(self.newWindow2, text='March',variable=radioValue, value=3)
        self.panel = tk.Label(self.newWindow2)  # initialize image panel
        self.panel.place(x=0,y=0)
        rdioOne.place(x=650,y=10)
        rdioTwo.place(x=650,y=30)
        rdioThree.place(x=650,y=50)
        labelValue = tk.Label(self.newWindow2, textvariable=radioValue)
        labelValue.place(x=650,y=70)
        self.dect_loop()
    def dect_loop(self):
        success, img = self.camera.read()  # 从摄像头读取照片
        if success:
            cv2.waitKey(10)   
            cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)#转换颜色从BGR到RGBA
            current_image = Image.fromarray(cv2image)#将图像转换成Image对象
            imgtk = ImageTk.PhotoImage(image=current_image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)
            if  self.prwrite_flag == 0 and self.write_flag == 1: # 寫入影格
                self.prwrite_flag = 1
                self.save_name = self.video_name + str(self.video_counter) + self.file_type
                self.out = cv2.VideoWriter(self.save_name, self.fourcc, self.FPS, (self._CAMERA_WIDTH,self._CAMERA_HEIGH))
                print('writing to ' + self.save_name)
            elif self.write_flag == 0 and self.prwrite_flag == 1: #關閉影片   
                self.prwrite_flag = 0
                self.video_counter = self.video_counter + 1
                print('finish')
                self.ShowMessage.insert('end', str(self.save_name)+'檔案已儲存\n')
            
            if (self.write_flag == 1):
               self.out.write(img)
    
        self.newWindow2.after(1, self.dect_loop)
    def Menu2(self):
        self.newWindow = tk.Toplevel(self)
        self.newWindow.geometry('1000x500')
        self.panel = tk.Label(self.newWindow)  # initialize image panel
        self.panel.place(x=0,y=0)

        download = tk.Button(self.newWindow, text=' 影片上傳 ',width=10,command=self.OpenFile)
        download.place(x=650,y=10)
        StartRecord = tk.Button(self.newWindow, text=' 開始錄影 ',width=10, command=self.Start)
        StartRecord.place(x=750,y=10)
        EndRecord = tk.Button(self.newWindow, text=' 結束錄影 ',width=10, command=self.End)
        EndRecord.place(x=850,y=10)
        scrollbar = tk.Scrollbar(self.newWindow)
        #scrollbar.place(x=1050,y=100)
        self.ShowMessage = tk.Text(self.newWindow,width=33, height=25, background = "black",foreground="white",yscrollcommand=scrollbar.set)
        for i in range(40):
             #插入內容到 listbox 尾端
             self.ShowMessage.insert('end', str(i)+"\n")
        # side='left' 放入左邊
        # fill='both' 向 x 軸和 y 軸填滿
        # expand=1 開啟 fill
        self.ShowMessage.place(x=650,y=50)
        # scrollbar 移動時使 listbox 跟著移動
        
        scrollbar.config(command=self.ShowMessage.yview)
        self.video_loop()
    def video_loop(self):
        success, img = self.camera.read()  # 从摄像头读取照片
        if success:
            cv2.waitKey(10)   
            cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)#转换颜色从BGR到RGBA
            current_image = Image.fromarray(cv2image)#将图像转换成Image对象
            imgtk = ImageTk.PhotoImage(image=current_image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)
            if  self.prwrite_flag == 0 and self.write_flag == 1: # 寫入影格
                self.prwrite_flag = 1
                self.save_name = self.video_name + str(self.video_counter) + self.file_type
                self.out = cv2.VideoWriter(self.save_name, self.fourcc, self.FPS, (self._CAMERA_WIDTH,self._CAMERA_HEIGH))
                print('writing to ' + self.save_name)
            elif self.write_flag == 0 and self.prwrite_flag == 1: #關閉影片   
                self.prwrite_flag = 0
                self.video_counter = self.video_counter + 1
                print('finish')
                self.ShowMessage.insert('end', str(self.save_name)+'檔案已儲存\n')
            
            if (self.write_flag == 1):
               self.out.write(img)
    
        self.newWindow.after(1, self.video_loop)
    def clearToTextInput(self):
        self.ShowMessage.delete("1.0","end")
    def Start(self):
        self.clearToTextInput()#-- 清空存放操作記錄的棧
        self.write_flag = 1
        self.ShowMessage.insert('end', '開始錄影\n')
        
    def End(self):
        self.write_flag = 0
        self.ShowMessage.insert('end', '結束錄影\n')
       
    def OpenFile(self):
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
if __name__ == "__main__":
    app = App()
    app.mainloop()