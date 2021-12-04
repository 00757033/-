# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 00:05:08 2021

@author: 翁培馨
"""
def highlight():
  import tkinter as tk, threading
  from tkinter import messagebox
  import imageio
  from PIL import Image, ImageTk
  from tkinter import filedialog
  import Highlight.point
  import os
  root = tk.Tk()
  root.title("please choose the video ")
  root.geometry('600x700')
  button_1 = tk.Button(root, text='Please select a video', bg='#4f74b0', fg='#263238',activebackground='#9D9D9D', font=('Arial', 16), command=lambda:[sure()]).place(x=100, y=100, height=80, width=400)
  #button_1.grid(column=10, row=10)
  def sure():

      root_choose = tk.Tk()
      root_choose.withdraw()
      file_path = filedialog.askopenfilename()
      try:
       video = imageio.get_reader(file_path)
       file_path=file_path[0:-4]
       os.makedirs('../../../../../../..'+file_path,exist_ok=True)
       root_choose.destroy()
       #shutil.rmtree('../../../../../../..'+file_path)
       button_2 = tk.Button(root, text='Sure', bg='#d4d64f', fg='#263238',activebackground='#9D9D9D', font=('Arial', 16), command=lambda:[Highlight.point.highlight(file_path)]).place(x=100, y=350, height=80, width=400)
       messagebox.showinfo('my messagebox', 'file will be at :\n'+file_path)
      except Exception as e:
        messagebox.showinfo('my messagebox', 'This is not a video file! Please try again!')

        #label = tk.Label(root,text='This is not a video file! Please try again!', bg='red').place(x=100, y=350, height=80, width=200)
    
    
    #button_2.grid(column=10, row=20)
  #root.destroy()
  root.mainloop()
