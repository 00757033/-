# -*- coding: utf-8 -*-
"""

Created on Mon Aug  2 23:21:19 2021

@author: 翁培馨
import speech_recognition as sr須連網

"""
try:
    
        import appControl
        import webScrapping
        from userHandler import UserData
        from FACE_UNLOCKER import clickPhoto, viewPhoto
        import angle
        import record_volleyball
except Exception as e:
	raise e
        
        
try:
        import os
        import speech_recognition as sr
        import pyttsx3
        from tkinter import *
        from tkinter import ttk
        from tkinter import messagebox
        from tkinter import colorchooser
        from PIL import Image, ImageTk
        from time import sleep
        from threading import Thread#cpu idel 可用不然聲音判定一直存在
except Exception as e:
	print(e)
chat_name ='S.S.A'.lower()#大寫轉小寫
EXIT_COMMANDS = ['掰掰','再見','bye','exit','quit','shut down', 'shutdown']
rec_email, rec_phoneno = "", ""#寄信用
train_lock=1
total_lock1=1
total_lock2=1
total_lock2_when=1
total_lock_make_up=1
total_lock0=1
train_squat=1

## 聊天字與顏色
WAEMEntry = None#?
avatarChoosen = 0#哪個腳色
choosedAvtrImage = None#腳色圖
ssaChatTextBg = "#007cc7"
ssaChatText = "white"
userChatTextBg = "#4da8da"
chatBgColor = '#b8b78d'
background = '#203647'
textColor = 'white'
CHATTaskStatusLblBG = '#203647'#鍵盤框顏色
KCS_IMG = 1 #0 for light, 1 for dark
voice_id = 0 #0 for female, 1 for male
ass_volume = 1 #max volume
ass_voiceRate = 200 #normal voice rate

print("start")
###################################### IMPORTING MODULES #####################################
""" User Created Modules """

    
########################################## LOGIN CHECK ##############################################
try:
    user = UserData()
    user.extractData()#獲取檔案
    ownerName = user.getName().split()[0]
    ownerDesignation = "先生"
    if user.getGender()=="Female": ownerDesignation = "小姐"
    ownerPhoto = user.getUserPhoto()
except Exception as e:
    print("You're not Registered Yet !\nRun SECURITY.py file to register your face.")
    raise SystemExit


########################################## BOOT UP WINDOW  ##############################################
def ChangeSettings(write=False):
    import pickle
    global background, textColor, chatBgColor, voice_id, ass_volume, ass_voiceRate, CHATTaskStatusLblBG, KCS_IMG, ssaChatTextBg, ssaChatText, userChatTextBg
    setting = {'background': background,
               'textColor': textColor,
				'chatBgColor': chatBgColor,
				'CHATTaskStatusLblBG': CHATTaskStatusLblBG,
				'KCS_IMG': KCS_IMG,
				'ssaChatText': ssaChatText,
				'ssaChatTextBg': ssaChatTextBg,
				'userChatTextBg': userChatTextBg,
				'voice_id': voice_id,
				'ass_volume': ass_volume,
				'ass_voiceRate': ass_voiceRate
                }
    if write:
        with open('userData/settings.pck', 'wb') as file:
            pickle.dump(setting, file)
            return
    try:
        with open('userData/settings.pck', 'rb') as file:
            loadSettings = pickle.load(file)
            background = loadSettings['background']
            textColor = loadSettings['textColor']
            chatBgColor = loadSettings['chatBgColor']
            CHATTaskStatusLblBG = loadSettings['CHATTaskStatusLblBG']
            KCS_IMG = loadSettings['KCS_IMG']
            ssaChatText = loadSettings['ssaChatText']
            ssaChatTextBg = loadSettings['ssaChatTextBg']
            userChatTextBg = loadSettings['userChatTextBg']
            voice_id = loadSettings['voice_id']
            ass_volume = loadSettings['ass_volume']
            ass_voiceRate = loadSettings['ass_voiceRate']
    except Exception as e:
            pass

if os.path.exists('userData/settings.pck')==False:
	ChangeSettings(True)
	
def getChatColor():
    global chatBgColor
    chatBgColor = myColor[1]
    colorbar['bg'] = chatBgColor
    chat_frame['bg'] = chatBgColor
    root1['bg'] = chatBgColor





ChangeSettings()

############################################ SET UP VOICE ###########################################
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id) #初始male 設置其聲音為pyttsx的函數
    engine.setProperty('volume', ass_volume)
except Exception as e:
    print(e)
####################################### SET UP TEXT TO SPEECH #######################################
def speak(text, display=False, icon=False):
    CHATTaskStatusLbl['text'] = 'spaeking'
    if icon: Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='w',pady=0)#左邊機器人說話的GUI　Label tkinter /ancho元件在容器中的錨定位置 : E, W, S, N, CENTER (預設), NE, SE, SW, NW / pady:元件邊框與容器之距離
    if display: attachTOframe(text, True)#?
    print('\n'+chat_name.upper()+': '+text)
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        print("Try not to type more...")
        
        
####################################### SET UP SPEECH TO TEXT #######################################
def record(clearChat=True, iconDisplay=True):
    print('\nListening...')
    CHATTaskStatusLbl['text'] = 'Listening...'
    r = sr.Recognizer()#預設辨識英文 speech_recognition as sr
    r.dynamic_energy_threshold = False#啟用了動態閾值，這將自動調整
    r.energy_threshold = 4000#用來敏感聲音度 無法識別可調整較低值
    with sr.Microphone() as source:# 錄音
        r.adjust_for_ambient_noise(source)# listen for 1 second to calibrate(校準) the energy threshold(能量阈值) for ambient noise levels(環境噪音levels)
        audio = r.listen(source)
        said = ""
        try:
            CHATTaskStatusLbl['text'] = '分析中......'
            said = r.recognize_google(audio,language="zh-TW")
            print(f"\nUser said: {said}")
            if clearChat:#刪除整個聊天紀錄
                clearChatScreen()
            if iconDisplay: Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e',pady=0)
            attachTOframe(said)
        except Exception as e:
            print(e)
            # speak("I didn't get it, Say that again please...")
            if "connection failed" in str(e):
                speak("Your System is Offline...", True, True)
                return 'None'
    return said.lower()#小寫

def voiceMedium():#中等
	while True:
		query = record()
		if query == 'None': continue
		if isContain(query, EXIT_COMMANDS):
			speak("Shutting down the System. Good Bye "+ownerDesignation+"!", True, True)
			break
		else: main(query.lower())#到main的def去測試要開什麼指令
	appControl.Win_Opt('close')#?
    

def keyboardInput(e):
    user_input = UserField.get().lower()#?輸入那攔輸入甚麼
    if user_input!="":
        clearChatScreen()#清畫面
        if isContain(user_input, EXIT_COMMANDS):
            speak("Shutting down the System. Good Bye "+ownerDesignation+"!", True, True)
        else:
            Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e',pady=0)
            attachTOframe(user_input.capitalize())
            Thread(target=main, args=(user_input,)).start()#呼叫所寫的 main 主程式 args = (url_list1,1) 是放你要給與 main 的參數 .start 這邊會依順序開始啟動線程t.start 這邊會依順序開始啟動線程
        UserField.delete(0, END)
###################################### TASK/COMMAND HANDLER #########################################
def isContain(txt, lst):#是否包含這個字
    for word in lst:
        if word in txt:
            return True
    return False
def main(text):
    global train_lock
    global total_lock1
    global total_lock2
    global total_lock2_when
    global total_lock_make_up
    global total_lock0
    global train_squat
    if 'email' in text:
            speak('Whom do you want to send the email?', True, True)
            WAEMPOPUP("Email", "E-mail Address")
            attachTOframe(rec_email)
            speak('What is the Subject?', True)
            subject = record(False, False)
            speak('What message you want to send ?', True)
            message = record(False, False)
            Thread(target=webScrapping.email, args=(rec_email,message,subject,) ).start()
            speak('Email has been Sent', True)
            return
#########自我訓練#########        
    if isContain(text, ['train','自我','訓練','練習','體能']) :
            speak('請輸入動作toss,serve,深蹲,仰臥起坐,棒式')
            train_lock=0#open
            return
    if train_lock==0:
        if isContain(text, ['toss','serve','仰臥起坐','深蹲']) :
            Thread(angle.training(text,0)) 
            train_lock=1
            return
        if isContain(text,['棒式']):
            train_squat=0
            train_lock=1
            speak('請輸入訓練秒數')
    if train_squat==0:
        Thread(angle.training('棒式',int(text)))
        train_squat=1

######## 圖表###########
    if isContain(text, ['圖表','結果','統整','紀錄','record']) :
        speak('請加入要那些動作')
        Thread(target=action_total.action).start()
        tota_lock1=0
        speak('完成後請輸入想查詢的格式時間太長不建議天數( 年/月/日)', True, True)
        
        return
    if isContain(text, ['gogo']):
        Thread(target=record_volleyball.total_start()).start()
        return
    result = normalChat.reply(text)
    if result != "None": speak(result, True, True)
    else:
        speak("Here's what I found on the web... ", True, True)
        #webScrapping.googleSearch(text)    
        
##################################### DELETE USER ACCOUNT #########################################
def deleteUserData():#刪除UserData 但試圖刪除謝謝
	result = messagebox.askquestion('Alert', 'Are you sure you want to delete your Face Data ?')
	if result=='no': return
	messagebox.showinfo('Clear Face Data', 'Your face has been cleared\nRegister your face again to use.')
	import shutil
	shutil.rmtree('userData')
	root.destroy()

						#####################
						####### GUI #########
						#####################  
                        
############ ATTACHING BOT/USER CHAT ON CHAT SCREEN ###########
def attachTOframe(text,ssa=False):#聊天室的字顯示
	if ssa:
		ssachat = Label(chat_frame,text=text, bg=ssaChatTextBg, fg=ssaChatText, justify=LEFT, wraplength=250, font=('Montserrat',12, 'bold'))#wraplength对于可以执行自动换行的小部件，此选项指定最大行长。超过此长度的行将被包装到下一行
		ssachat.pack(anchor='w',ipadx=5,ipady=5,pady=5)#
	else:
		userchat = Label(chat_frame, text=text, bg=userChatTextBg, fg='white', justify=RIGHT, wraplength=250, font=('Montserrat',12, 'bold'))
		userchat.pack(anchor='e',ipadx=2,ipady=2,pady=5)

def clearChatScreen():
	for wid in chat_frame.winfo_children():
		wid.destroy()

### SWITCHING BETWEEN FRAMES ###?
def raise_frame(frame):
	frame.tkraise()
	clearChatScreen()
############################# SHOWING DOWNLOADED IMAGES ##############################暫時用不到
img0, img1, img2, img3, img4 = None, None, None, None, None
def showSingleImage(type, data=None):
	global img0, img1, img2, img3, img4
	try:
		img0 = ImageTk.PhotoImage(Image.open('Downloads/0.jpg').resize((90,110), Image.ANTIALIAS))
	except:
		pass
	img1 = ImageTk.PhotoImage(Image.open('extrafiles/images/heads.jpg').resize((220,200), Image.ANTIALIAS))
	img2 = ImageTk.PhotoImage(Image.open('extrafiles/images/tails.jpg').resize((220,200), Image.ANTIALIAS))
	img4 = ImageTk.PhotoImage(Image.open('extrafiles/images/WeatherImage.png'))

	if type=="weather":
		weather = Frame(chat_frame)
		weather.pack(anchor='w')
		Label(weather, image=img4, bg=chatBgColor).pack()
		Label(weather, text=data[0], font=('Arial Bold', 45), fg='white', bg='#3F48CC').place(x=65,y=45)
		Label(weather, text=data[1], font=('Montserrat', 15), fg='white', bg='#3F48CC').place(x=78,y=110)
		Label(weather, text=data[2], font=('Montserrat', 10), fg='white', bg='#3F48CC').place(x=78,y=140)
		Label(weather, text=data[3], font=('Arial Bold', 12), fg='white', bg='#3F48CC').place(x=60,y=160)

	elif type=="wiki":
		Label(chat_frame, image=img0, bg='#EAEAEA').pack(anchor='w')
	elif type=="head":
		Label(chat_frame, image=img1, bg='#EAEAEA').pack(anchor='w')
	elif type=="tail":
		Label(chat_frame, image=img2, bg='#EAEAEA').pack(anchor='w')
	else:
		img3 = ImageTk.PhotoImage(Image.open('extrafiles/images/dice/'+type+'.jpg').resize((200,200), Image.ANTIALIAS))
		Label(chat_frame, image=img3, bg='#EAEAEA').pack(anchor='w')
	
def showImages(query):
	global img0, img1, img2, img3
	webScrapping.downloadImage(query)
	w, h = 150, 110
	#Showing Images
	imageContainer = Frame(chat_frame, bg='#EAEAEA')
	imageContainer.pack(anchor='w')
	#loading images
	img0 = ImageTk.PhotoImage(Image.open('Downloads/0.jpg').resize((w,h), Image.ANTIALIAS))
	img1 = ImageTk.PhotoImage(Image.open('Downloads/1.jpg').resize((w,h), Image.ANTIALIAS))
	img2 = ImageTk.PhotoImage(Image.open('Downloads/2.jpg').resize((w,h), Image.ANTIALIAS))
	img3 = ImageTk.PhotoImage(Image.open('Downloads/3.jpg').resize((w,h), Image.ANTIALIAS))
	#Displaying
	Label(imageContainer, image=img0, bg='#EAEAEA').grid(row=0, column=0)
	Label(imageContainer, image=img1, bg='#EAEAEA').grid(row=0, column=1)
	Label(imageContainer, image=img2, bg='#EAEAEA').grid(row=1, column=0)
	Label(imageContainer, image=img3, bg='#EAEAEA').grid(row=1, column=1)

############################# WAEM - WhatsApp Email ##################################
def sendWAEM():
	global rec_phoneno, rec_email
	data = WAEMEntry.get()
	rec_email, rec_phoneno = data, data
	WAEMEntry.delete(0, END)### CLear a TKinter box=WAEMEntry
	appControl.Win_Opt('close')#關
def send(e):
	sendWAEM()

def WAEMPOPUP(Service='None', rec='Reciever'):
	global WAEMEntry
	PopUProot = Tk()#設TK()
	PopUProot.title(f'{Service} Service')
	PopUProot.configure(bg='white')

	if Service=="WhatsApp": PopUProot.iconbitmap("extrafiles/images/whatsapp.ico")
	else: PopUProot.iconbitmap("extrafiles/images/email.ico")#email
	w_width, w_height = 410, 200
	s_width, s_height = PopUProot.winfo_screenwidth(), PopUProot.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	PopUProot.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
	Label(PopUProot, text=f'Reciever {rec}', font=('Arial', 16), bg='white').pack(pady=(20, 10))
	WAEMEntry = Entry(PopUProot, bd=10, relief=FLAT, font=('Arial', 12), justify='center', bg='#DCDCDC', width=30)
	WAEMEntry.pack()
	WAEMEntry.focus()

	SendBtn = Button(PopUProot, text='Send', font=('Arial', 12), relief=FLAT, bg='#14A769', fg='white', command=sendWAEM)
	SendBtn.pack(pady=20, ipadx=10)
	PopUProot.bind('<Return>', send)#按ENTER了
	PopUProot.mainloop()                        
######################## CHANGING CHAT BACKGROUND COLOR #########################
def getChatColor():
	global chatBgColor
	myColor = colorchooser.askcolor()
	if myColor[1] is None: return
	chatBgColor = myColor[1]
	colorbar['bg'] = chatBgColor
	chat_frame['bg'] = chatBgColor
	root1['bg'] = chatBgColor
	ChangeSettings(True)

chatMode = 1
def changeChatMode():
	global chatMode
	if chatMode==1:
		# appControl.volumeControl('mute')
		VoiceModeFrame.pack_forget()
		TextModeFrame.pack(fill=BOTH)
		UserField.focus()
		chatMode=0
	else:
		# appControl.volumeControl('full')
		TextModeFrame.pack_forget()
		VoiceModeFrame.pack(fill=BOTH)
		root.focus()
		chatMode=1

############################################## GUI #############################################



#####################################  MAIN GUI ####################################################

#### SPLASH/LOADING SCREEN ####
def progressbar():#前面的PROCESSIMG
	s = ttk.Style()
	s.theme_use('clam')
	s.configure("white.Horizontal.TProgressbar", foreground='white', background='white')
	progress_bar = ttk.Progressbar(splash_root,style="white.Horizontal.TProgressbar", orient="horizontal",mode="determinate", length=303)
	progress_bar.pack()
	splash_root.update()
	progress_bar['value'] = 0
	splash_root.update()
 
	while progress_bar['value'] < 100:#跑到100
		progress_bar['value'] += 5
		# splash_percentage_label['text'] = str(progress_bar['value']) + ' %'
		splash_root.update()
		sleep(0.1)

def destroySplash():
	splash_root.destroy()#關閉視窗
	splash_root.quit()#關閉視窗

#if __name__ == '__main__':
print("root")

splash_root = Tk()#前面的PROCESSIMG
splash_root.configure(bg='#3895d3')
splash_root.overrideredirect(True)#overrideredirect將視窗的邊框消失
splash_label = Label(splash_root, text="Processing...", font=('montserrat',15),bg='#0f8567',fg='white')
splash_label.pack(pady=40)
   	# splash_percentage_label = Label(splash_root, text="0 %", font=('montserrat',15),bg='#3895d3',fg='white')
   	# splash_percentage_label.pack(pady=(0,10))
   
w_width, w_height = 400, 200
s_width, s_height = splash_root.winfo_screenwidth(), splash_root.winfo_screenheight()
x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
splash_root.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30))
   
progressbar()#用來跑得像跑了100趴
#splash_root.after(10, destroySplash)#10秒 消除
splash_root.after(1, destroySplash)
splash_root.mainloop()	
   
root = Tk()#主
root.title('F.R.I.D.A.Y')
w_width, w_height = 400, 650
s_width, s_height = root.winfo_screenwidth(), root.winfo_screenheight()
x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
root.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
root.configure(bg=background)
   	# root.resizable(width=False, height=False)
root.pack_propagate(0)
   
root1 = Frame(root, bg='#b8b78d')
root2 = Frame(root, bg='#c91616')
root3 = Frame(root, bg='#16c9af')#聊天視窗
   
for f in (root1, root2, root3):
    print('539')
    f.grid(row=0, column=0, sticky='news')	
   	
   	################################
   	########  CHAT SCREEN  #########
   	################################
   
   	#Chat Frame
chat_frame = Frame(root1, width=380,height=551,bg=chatBgColor)
chat_frame.pack(padx=10)
chat_frame.pack_propagate(0)
   
bottomFrame1 = Frame(root1, bg='#dfdfdf', height=100)
bottomFrame1.pack(fill=X, side=BOTTOM)
VoiceModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
VoiceModeFrame.pack(fill=BOTH)
TextModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
TextModeFrame.pack(fill=BOTH)
   
   	# VoiceModeFrame.pack_forget()
TextModeFrame.pack_forget()
   
cblLightImg = PhotoImage(file='extrafiles/images/centralButton.png')
cblDarkImg = PhotoImage(file='extrafiles/images/centralButton.png')
if KCS_IMG==1: cblimage=cblDarkImg
else: cblimage=cblLightImg
cbl = Label(VoiceModeFrame, fg='white', image=cblimage, bg='#dfdfdf')
cbl.pack(pady=17)
CHATTaskStatusLbl = Label(VoiceModeFrame, text='    Offline', fg='white', bg=CHATTaskStatusLblBG, font=('montserrat', 16))
CHATTaskStatusLbl.place(x=140,y=32)
   	


   	
   	#Keyboard Button
kbphLight = PhotoImage(file = "extrafiles/images/keyboard.png")
kbphLight = kbphLight.subsample(2,2)
kbphDark = PhotoImage(file = "extrafiles/images/keyboard1.png")
kbphDark = kbphDark.subsample(2,2)
if KCS_IMG==1: kbphimage=kbphDark
else: kbphimage=kbphLight
kbBtn = Button(VoiceModeFrame,image=kbphimage,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf", command=changeChatMode)
kbBtn.place(x=25, y=30)
   
   	#Mic
micImg = PhotoImage(file = "extrafiles/images/mic.png")
micImg = micImg.subsample(2,2)
micBtn = Button(TextModeFrame,image=micImg,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf", command=changeChatMode)
micBtn.place(relx=1.0, y=30,x=-20, anchor="ne")	
   	
#Text Field
TextFieldImg = PhotoImage(file='extrafiles/images/textField.png')
UserFieldLBL = Label(TextModeFrame, fg='white', image=TextFieldImg, bg='#dfdfdf')
UserFieldLBL.pack(pady=17, side=LEFT, padx=10)
UserField = Entry(TextModeFrame, fg='white', bg='#203647', font=('Montserrat', 16), bd=6, width=22, relief=FLAT)
UserField.place(x=20, y=30)
UserField.insert(0, "Ask me anything...")
UserField.bind('<Return>', keyboardInput)
   	
   	#User and Bot Icon
userIcon = PhotoImage(file="extrafiles/images/avatars/ChatIcons/a"+str(ownerPhoto)+".png")
botIcon = PhotoImage(file="extrafiles/images/assistant2.png")
botIcon = botIcon.subsample(2,2)
   	

   
try:
   		# pass
   		Thread(target=voiceMedium).start()
except:
   		pass
try:
   		# pass
   		Thread(target=webScrapping.dataUpdate).start()
except Exception as e:
   		print('System is Offline...')
   	
root.iconbitmap('extrafiles/images/assistant2.ico')
raise_frame(root1)
root.mainloop()                        

                       
                       
                       
                       
                       
                       
                       
                       
                       
                       
                       