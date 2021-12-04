from tkinter import *
from PIL import Image,ImageTk
import tkinter.ttk as ttk
import os
import cv2
import datetime
import re

def record():
    def quit():
        root.destroy()
    # function
    def combobox_selected(event):
        print(my_combobox.current(), my_combobox.get())
        my_list.delete(0, END)
        for filename in os.listdir('Record/video/'):
            file = re.split('[_.]', filename)
            if file[0] == my_combobox.get() and my_combobox.current() != 0:
                my_list.insert(END, filename)
            elif my_combobox.get() == 'select action':
                my_list.insert(END, filename)

    # function
    def delete_item():
        for index in my_list.curselection()[::-1]:
            os.remove("Record/video/" + my_list.get(index))
            my_list.delete(index)

    def dbclick(event):
        index = my_list.curselection()
        print(my_list.get(index))
        cap = cv2.VideoCapture('Record/video/' + my_list.get(index))
        #fps= int(cap.get(cv2.CAP_PROP_FPS))
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            #time.sleep(1/fps)
            cv2.imshow('frame', frame)
            if cv2.waitKey(15) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    # time: today
    loc_dt = datetime.datetime.today()
    time_del = datetime.timedelta(weeks=8)
    new_dt = loc_dt - time_del
    today_time = loc_dt.strftime('%Y-%m-%d %H-%M-%S')
    deadline_time = new_dt.strftime('%Y-%m-%d %H-%M-%S')
    print(today_time)
    print(deadline_time)

    root = Tk()
    root.title('Record')
    root.geometry("500x500")

    # Create Combobox
    my_combobox = ttk.Combobox(root, font=("Times", 18),width=28, height=10)
    my_combobox['values'] = ['select action', 'toss', 'serve']
    my_combobox.pack(pady=10)
    my_combobox.current(0)
    my_combobox.bind('<<ComboboxSelected>>', combobox_selected)
    root.option_add("*Font",("Times", 18))
    # create frame
    my_frame = Frame(root)
    my_frame.pack(pady=10)

    # create listbox
    my_list = Listbox(my_frame, selectmode=EXTENDED, font=("Times", 18),width=28, height=10, bg="gray85", bd=0, fg="#464646", highlightthickness=0, selectbackground="#bc8f8f", activestyle="none")
    my_list.pack(side=LEFT, fill=BOTH)

    # add dummy list to list box
    for filename in os.listdir('Record/video/'):
        file_time = re.split('[_.]', filename)
        if file_time[1] > deadline_time:
            my_list.insert(END, filename)
        else:
            os.remove("Record/video/" + filename)

    # create scrollbar
    my_scrollbar = Scrollbar(my_frame)
    my_scrollbar.pack(side=RIGHT, fill=BOTH)

    # add scrollbar
    my_list.config(yscrollcommand=my_scrollbar.set)
    my_scrollbar.config(command=my_list.yview)

    # create button frame
    button_frame = Frame(root)
    button_frame.pack(pady=20)

    # double click item
    my_list.bind('<Double-1>', dbclick)

    exitimg = Image.open('pic/exit.png')
    exitimg = exitimg.resize((25, 25))
    global tkexitimg
    tkexitimg = ImageTk.PhotoImage(exitimg)
    # add button
    #exit_button = Button(button_frame, text="Exit",font=("Times", 20),activebackground='#9D9D9D',bg='#B87070',image=tkexitimg,compound = LEFT, command = quit)
    #exit_button.grid(row=0, column=0, padx=20)
    delete_button = Button(button_frame, text="Delete Item",font=("Times", 20),activebackground='#9D9D9D',bg='#5f9ea0', command=delete_item)
    delete_button.grid(row=0, column=1)

    root.mainloop()

if __name__ == '__main__': 
  record()

