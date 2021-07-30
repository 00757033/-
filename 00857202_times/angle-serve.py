# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 05:04:03 2021

@author: User
"""
# -*- coding: utf-8 -*-
"""
深蹲:
    側面 左右用或
    腳後跟不可起來
    step1->stand well
    step2->身體屁股腳的角度150
    count=60(不確定)速度不可太快
    step3->身體屁股腳的角度>40<100??
    if !肩膀、臀部& 地板角度50~70(30 32 點)=  wrong
    if !角度肩膀、臀部 膝蓋 - 角度臀部 膝蓋 腳踝 <20 wrong
    if !角度臀部 膝蓋 - 角度3032<20(要平行
仰臥起坐:
    setp1:
        腳彎曲
        躺平
        if 手放脖子後 wrong
    step2:仰臥起坐 肩膀與臀部與肩膀x臀部y>20
棒式:(幾組 先不做)
Stick
    時間
    手成90度
        手放肩膀下方
            肩膀 腳踝 與肩膀x 腳踝y>20
                膝蓋不能落第
                
                    start step1
    if step1 手成90度
        end<time fail
    if step1 手放肩膀下方
        end<time fail
    if step1 肩膀 腳踝 與肩膀x 腳踝y>20
        end<time fail
    if step1 膝蓋不能落第
        end<time fail
    if step1
        end
        if end>time
            success
            +time
            q
    
        
        
        
Created on Wed Jul 14 01:43:20 2021

@author: User
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 22:00:42 2021

@author: 00857202翁培馨

"""
import time
try:
    import time
    import cv2
    import mediapipe as mp
    import numpy as np
    import tkinter as tk
    import math
    import json
    import ast
    import base64
    import matplotlib.pylab as plt
    from datetime import datetime
    import os
    import subprocess
    from pynput.keyboard import Key, Controller
    import psutil
    import pyscreenshot as ImageGrab
    import pyttsx3
    from threading import Thread
except Exception as e:
	print(e)
# voice
engine = pyttsx3.init()
def speak(text):
   	print('\n'+text)
   	try:
   		engine.say(text)
   		engine.runAndWait()
   	except:
   		print("Try not to type more...")
   		print("123")
lock=0
stick_lock=0
data=dict()
no_makeup_data=dict()
action=dict()
root = tk.Tk()
count=-1

first_time=1
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
#print(screen_height)
#0x軸 1y軸
#下1 上0
#右1 左0
#  Make Detections
while (1):
    action=input("請輸入動作action:toss serve 深蹲 仰臥起坐")
    print(action)
    if action=="棒式":
        your_goal_time=input("請輸入棒式的時間")
        countfault=int(your_goal_time)/3
        break
    if action=="toss" or action=="serve" or action=="深蹲" or action=="仰臥起坐":
        break
    
    

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)

# Curl counter variables
count321=0
start0 = time.time()
close1=0
close2=0
close3=0
counter = 0 
counter_serve = 0 
counter_squat = 0 
counter_situp = 0 
counter_stick=0

stage = None
serve_stage = None
squat_stage= None
situp_stage= None
stick_stage= None
def calculate_angle(a,b,c):#順時
#https://blog.csdn.net/songyunli1111/article/details/81145971
#angle = atan( (y2-y1)/(x2-x1) )或angle = atan2( y2-y1, x2-x1 ) atan 为单个参数，atan2为两个参数如果 x2-x1等于0 ，角度依然可以计算
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])#弧度
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 
def calculate_angle2(a,b,c):#for 肩膀、臀部& 地板角度50~70(30 32 點) 將right_foot_index y軸設為hip
#https://blog.csdn.net/songyunli1111/article/details/81145971
#angle = atan( (y2-y1)/(x2-x1) )或angle = atan2( y2-y1, x2-x1 ) atan 为单个参数，atan2为两个参数如果 x2-x1等于0 ，角度依然可以计算
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(b[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])#弧度
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 
def calculate_angle3(a,b,c):#棒式身體的balance腳踝   頭在螢幕左側要正規花手的三倍為ankle
#calculate_angle3( left_elbow,left_foot_index,left_shoulder)
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    #print("abs(np.arctan2(c[1]-b[1], c[0]-b[0]))",abs(np.arctan2(c[1]-a[1], c[0]-a[0])))#這是斜率不是長度拉
    #print("c[0]",c[0])
    #print("b[0]",b[0])
    #print("b[0]=c[0]-3*abs(c[1]-a[1])",c[0]-3*abs(c[1]-a[1]))
    if c[0]<b[0]:
        b[0]=c[0]+3*abs(c[1]-a[1])
    else:
        b[0]=c[0]-3*abs(c[1]-a[1])
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(b[1]-b[1], c[0]-b[0])#弧度
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 
def calculate_angle4(a,b,c):#for仰臥起坐 肩膀與臀部與肩膀x臀部y   頭在螢幕右側
#situp_lefthand_hip_angle = calculate_angle4( left_shoulder,left_hip,left_ankle)#

    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    
    radians = np.arctan2(b[1]-b[1], a[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])#弧度
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle
## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        
        
        check=0
        ret, frame = cap.read()
        if ret==True:#水平翻轉
            frame = cv2.flip(frame,180)
            
            
            # frame = cv2.flip(frame,0)
           	# Start time
            
            
            
        else:
            break
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates # elbow 手肘 wrist 手腕 #hip屁股 
            nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,landmarks[mp_pose.PoseLandmark.NOSE.value].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            right_ear = [landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].x,landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].y]
            right_index = [landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y]
            right_heel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
            right_foot_index = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
            
            left_heel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
            left_foot_index = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
            left_index = [landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            left_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            left_ear = [landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].y]
            
            # Calculate angle toss
            toss_lefthand_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)#手的角度
            toss_lefthand_shoulder_angle = calculate_angle( left_elbow,left_shoulder,left_hip)#身體到手的角度
            toss_righthand_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            toss_righthand_shoulder_angle = calculate_angle( right_elbow,right_shoulder,right_hip)
            
            if left_ankle[1]<1 and left_ankle[1]>0 and left_ankle[1]<1 and left_ankle[1]>0 and nose[1]<1 and nose[1]>0 and left_index[0]>0 and left_index[0]<1 and right_index[0]>0 and right_index[0]<1:
                toss_leftheight = abs(nose[1]-left_ankle[1])*100
                toss_rightheight =abs(nose[1]-right_ankle[1])*100
                check=1#stand well
                
            else:
                check=0
                cv2.putText(image, str("stand well"), 
                           tuple(np.multiply(left_shoulder, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 10, cv2.LINE_AA
                                )
            
            
            # Calculate angle serve
            serve_lefthand_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            serve_righthand_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            serve_righthand_shoulder_angle = calculate_angle(right_elbow,right_shoulder,right_hip)
            serve_lefthand_shoulder_angle = calculate_angle(left_elbow,left_shoulder,left_hip)
            serve_righthand_higherthan_ear=right_ear[1]-right_wrist[1]
            serve_lefthand_higherthan_ear=left_ear[1]-left_wrist[1]
            serve_righthand_higherthan_shoulder=right_shoulder[1]-right_wrist[1] #>0代表手舉高
            serve_lefthand_higherthan_shoulder=left_shoulder[1]-left_wrist[1]
            # Visualize angle
            #print(serve_righthand_higherthan_ear)
            
            
            # Calculate angle 深蹲
            
            squat_lefthand_hip_angle = calculate_angle( left_shoulder,left_hip,left_knee)#
            squat_righthand_hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)
            squat_lefthand_knee_angle = calculate_angle( left_hip,left_knee,left_ankle)#
            squat_righthand_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
            squat_righthand_body_angle = calculate_angle2(right_shoulder, right_hip, right_foot_index)#上半身過度前傾： 因為深蹲時重心向後移，人會下意識地往前傾來平衡，但正確姿勢建議肩膀、下背、臀部成一直線，並與地面夾50~70度，即使膝蓋因此稍微超過腳尖也沒關係。
            squat_leftthand_body_angle = calculate_angle2(left_shoulder,left_hip, left_foot_index)#上半身過度前傾： 因為深蹲時重心向後移，人會下意識地往前傾來平衡，但正確姿勢建議肩膀、下背、臀部成一直線，並與地面夾50~70度，即使膝蓋因此稍微超過腳尖也沒關係。
            squat_righthand_balance_angle = calculate_angle2(right_hip, right_knee, right_foot_index)#角度臀部 膝蓋 - 角度3032<20(要平行
            squat_lefthand_balance_angle = calculate_angle2(left_hip, left_knee, left_foot_index)#角度臀部 膝蓋 - 角度3032<20(要平行
            cv2.putText(image, str(squat_lefthand_knee_angle), 
                           tuple(np.multiply(left_knee, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            
            
            
            
            
            
             # Calculate angle 仰臥起坐
            
            situp_lefthand_hip_angle = calculate_angle4( left_shoulder,left_hip,left_ankle)#
            situp_righthand_hip_angle = calculate_angle4(right_shoulder, right_hip, right_ankle)
            situp_lefthand_knee_angle = calculate_angle( left_hip,left_knee,left_ankle)#肩膀 腳趾 與肩膀x 腳踝y>40
            situp_righthand_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
           
            
           
            
           
            
           
            # Calculate angle 棒式
            
            stick_lefthand_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)#80-100
            stick_righthand_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            stick_lefthand_knee_angle = calculate_angle( left_hip,left_knee,left_ankle)#
            stick_righthand_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)#>160
            stick_lefthand_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
            stick_lefthand_balance_angle = calculate_angle3( left_elbow,left_foot_index,left_shoulder)#>40
            stick_righthand_balance_angle = calculate_angle3( right_elbow,right_foot_index,right_shoulder)
            # left_ankle >left_knee>right_hip>right_shoulder
            
            
            stick_lefthand_elbow_angle_wrong = calculate_angle(left_shoulder, left_elbow, left_wrist)#80-100
            stick_righthand_elbow_angle_wrong = calculate_angle(right_shoulder, right_elbow, right_wrist)
            stick_lefthand_knee_angle_wrong = calculate_angle( left_hip,left_knee,left_ankle)#
            stick_righthand_knee_angle_wrong = calculate_angle(right_hip, right_knee, right_ankle)#>160
            stick_lefthand_knee_angle_wrong = calculate_angle(left_hip, left_knee, left_ankle)
            stick_lefthand_balance_angle_wrong = calculate_angle3( left_hip,left_foot_index,left_shoulder)#>40
            stick_righthand_balance_angle_wrong = calculate_angle3( right_hip,right_foot_index,right_shoulder)
            
            
            '''
            # Visualize angle
            cv2.putText(image, str(toss_lefthand_shoulder_angle), 
                           tuple(np.multiply(left_shoulder, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            # Visualize angle
            cv2.putText(image, str(toss_righthand_elbow_angle), 
                           tuple(np.multiply(right_elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            # Visualize angle
            cv2.putText(image, str( toss_righthand_shoulder_angle), 
                           tuple(np.multiply(right_shoulder, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
    
                # Visualize angle
            cv2.putText(image, str(toss_rightleg_1_angle), 
                           tuple(np.multiply(right_knee, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            # Visualize angle
            cv2.putText(image, str( toss_leftleg_1_angle), 
                           tuple(np.multiply(right_knee, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            
            '''
            end0 = time.time()
            # Time elapsed
            seconds0 = end0 - start0 
            #print( "Time takenall : {0} seconds".format(seconds0))
            if seconds0>=1 and close3==0:
                speak("三")
                close3=1
                
            if seconds0>=2 and close2==0:
                speak("二")
                close2=1
            if seconds0>=3 and close1==0:
                speak("一")
                speak("開始")
                close1=1
                count321=1
            if  check==0:
               serve_stage = "wait"
               stage = "wait"
            if action=="toss" and check==1 and count321==1:
                if toss_lefthand_elbow_angle < 90 and toss_lefthand_shoulder_angle > 80 and toss_righthand_elbow_angle < 90 and toss_righthand_shoulder_angle > 80 :
                    stage = "down"
                if first_time==1 or count <0:
                    #print("here")
                    count=25
                    heightl1=toss_leftheight
                    heightr1=toss_rightheight
                    first_time=0
                    #print(stage)
                    first_time=0
                else:
                    #print("count--",count)
                    count=count-1
                #print("toss",heightl1)    
                #print("toss2",heightl1-toss_leftheight)
                #print("hip",abs(left_hip[0]-right_hip[0])*100)
                if toss_lefthand_elbow_angle > 160 and toss_lefthand_shoulder_angle > 160 and toss_righthand_elbow_angle > 160 and toss_righthand_shoulder_angle > 160 and toss_leftheight-heightl1>abs(left_hip[0]-right_hip[0])*20 and stage =='down':
                    stage="up"
                    counter +=1
                    #print(stage)
                    #print(abs(left_hip[0]-right_hip[0])*100)
                    #print(counter)
                    first_time=1
                

                # Curl counter logic
            if action=="serve"and check==1 and count321==1:
                if serve_righthand_elbow_angle >130 and serve_lefthand_shoulder_angle >80 and serve_righthand_higherthan_ear<0 and serve_lefthand_higherthan_ear>0 and count <0:#預備動作
                    #
                    print("step1")
                    print(count)
                    serve_stage = "step1"
    
                if serve_righthand_higherthan_ear>0   and serve_righthand_elbow_angle >150 and serve_lefthand_higherthan_ear>0   and serve_stage =='step1':#拋球 兩手皆要超過耳朵
                    count=40
                    serve_stage="step2"
                    print("step2")
                    print(count)
    
                if  serve_lefthand_higherthan_ear<0  and serve_lefthand_elbow_angle >150  and serve_stage =='step2':
                    serve_stage="step3"
                    counter_serve +=1
                    count=-1
                    #print("step3")
                    #print(counter_serve)
                if serve_stage =='step2' or serve_stage =='step3':
                    count=count-1
                
                
                
                
            if action=="深蹲"and check==1 and (left_knee[1]<1 and left_knee[1]>0)  and (left_hip[1]<1 and left_hip[1]>0) and (left_shoulder[1]<1 and left_shoulder[1]>0) and count321==1:
                #speak(text)
                #print("lock",lock)
                #("squat_lefthand_knee_angle",squat_lefthand_knee_angle)
                #print("squat_stage",squat_stage)
                #speak("請轉側面")
                
                if (squat_lefthand_knee_angle <180 and squat_lefthand_knee_angle >=160 and lock==0) or (squat_righthand_knee_angle <180 and squat_righthand_knee_angle >=160 and lock==0):
                    print("start")
                    start = time.time()
                    print(lock)
                    #print(squat_lefthand_knee_angle)
                    save=0
                    lock=0
                    
                    squat_stage = "step1"
                if (squat_lefthand_knee_angle <160 and squat_lefthand_knee_angle >=150 and lock==0 and squat_stage !='step3'and squat_stage =='step1') or (squat_righthand_knee_angle <160 and squat_righthand_knee_angle >=150 and lock==0 and squat_stage !='step3'and squat_stage =='step1') :
                    
                    
                    print("step2")
                    print(lock)
                    squat_stage = "step2"
                    
    
                if (squat_lefthand_knee_angle <90 and squat_lefthand_knee_angle > 40 and lock==0  and squat_stage =='step2')or (squat_righthand_knee_angle<90 and squat_righthand_knee_angle>40 and lock==0  and squat_stage =='step2') :
                    if (left_foot_index[1]-left_heel[1]<abs(left_foot_index[0]-left_heel[0])/3)or (right_foot_index[1]-right_heel[1]<abs(right_foot_index[0]-right_heel[0])/3):
                        
                        end = time.time()
                        # Time elapsed
                        seconds = end - start 
                        print( "Time taken1 : {0} seconds".format(seconds))
                        if seconds<0.5:
                            speak("做太快了請重來")
                            squat_stage = "step1"
                        print("step3-1")
                        if (squat_righthand_body_angle >40 and squat_righthand_body_angle <80 and squat_stage !='step1' and lock==0) or(squat_leftthand_body_angle >40 and squat_leftthand_body_angle <80 and squat_stage !='step1' and lock==0) :
                            if abs(squat_lefthand_hip_angle - squat_lefthand_knee_angle<20 and lock==0)or (abs(squat_righthand_hip_angle - squat_righthand_knee_angle)<20 and lock==0):
                                if (left_foot_index[1]-left_heel[1]<abs(left_foot_index[0]-left_heel[0])/3 and lock==0)or (right_foot_index[1]-right_heel[1]<abs(right_foot_index[0]-right_heel[0])/3 and lock==0):
                                   
                                    
                                   squat_stage="step3"
                                   print("step3-2")
                                                                          
                                   lock=1
                                   print(lock)
    
                                else:
                                    Thread(speak("後腳跟不可抬起 "))
                            else:
                                Thread(speak("背部與小腿盡量平行 "))
                        
                        else:
                            Thread(speak("背 與 地板角度需介於50-80之間 "))
                    else:
                        squat_stage = "step1"
                        Thread(speak("後腳跟不可抬起  請重來"))
                    
                if (squat_righthand_body_angle >50 and squat_righthand_body_angle <80 and lock==1) or(squat_leftthand_body_angle >50 and squat_leftthand_body_angle <80 and lock==1):
                    #speak("到了")
                    start2 = time.time()
                    print(start2)
                if (squat_lefthand_knee_angle <180 and squat_lefthand_knee_angle >=160 and lock==1 and squat_stage =='step3') or (squat_righthand_knee_angle <180 and squat_righthand_knee_angle >=160 and lock==1 and squat_stage =='step3') :#or (squat_righthand_knee_angle <180 and squat_righthand_knee_angle >=160))
                    lock=0
                    if (left_foot_index[1]-left_heel[1]<abs(left_foot_index[0]-left_heel[0])/3)or (right_foot_index[1]-right_heel[1]<abs(right_foot_index[0]-right_heel[0])/3):
                        end2 = time.time()
                        # Time elapsed
                        seconds2 = end2 - start2
                        
                        print( "Time taken2 : {0} seconds".format(seconds2))
                        if seconds2<0.5:
                            squat_stage = "step1"
                            speak("做太快了請重來")
                            save=1
                            lock=0
                        else:
                            print("step4")
                            count=5
                            count2=0
                            squat_stage = "step4"
                            print(lock)
                            if save==0 :
                                save=1
                                counter_squat=counter_squat+1
                                Thread(speak(str(counter_squat)))
                                Thread(speak("次完成"))
                        
                    else:
                        Thread(speak("後腳跟不可抬起 請重來"))
                        squat_stage = "step1" 
                                                          
                    
                        
                

            
            
            if action=="仰臥起坐"and check==1 and (left_knee[1]<1 and left_knee[1]>0)  and (left_hip[1]<1 and left_hip[1]>0) and (left_shoulder[1]<1 and left_shoulder[1]>0) and count321==1:
                print("situp_lefthand_hip_angle",situp_lefthand_hip_angle)
                print("situp_lefthand_knee_angle",situp_lefthand_knee_angle)
                if (situp_lefthand_knee_angle<100 and situp_lefthand_hip_angle<5) or (situp_righthand_knee_angle<100 and situp_righthand_hip_angle<5):#預備動作
                    lock_situp=1
                    print("step1")
                    situp_stage = "step1"
                    
                
    
                if (situp_lefthand_knee_angle<100 and situp_lefthand_hip_angle>20) or (situp_righthand_knee_angle<100 and situp_righthand_hip_angle>20) and situp_stage != "wait"and squat_stage =='step1':#預備動作
                    if lock_situp==1:
                        counter_situp=counter_situp+1
                        lock_situp=0
                        
                    
                    situp_stage = "step2"
                    print(situp_stage)
                    #print(situp_lefthand_hip_angle)
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                
            if action=="棒式"and check==1 and (left_knee[1]<1 and left_knee[1]>0)  and (left_hip[1]<1 and left_hip[1]>0) and (left_shoulder[1]<1 and left_shoulder[1]>0) and count321==1:
                print("left_shoulder,left_foot_index",left_shoulder[1]," ",left_foot_index[1]," , ",left_shoulder[0]," ",left_foot_index[0])
                print("stick_lefthand_balance_angle",stick_lefthand_balance_angle)
                print("stick_lefthand_elbow_angle",stick_lefthand_elbow_angle)
                print("abs(left_shoulder[0]-left_elbow[0])<abs(left_foot_index[1]-left_heel[1])",abs(left_shoulder[0]-left_elbow[0]),"  ",abs(left_foot_index[1]-left_heel[1]))
                print("left_foot_index[1] >left_knee[1] and left_knee[1] >left_hip[1]",left_foot_index[1] ," ",left_knee[1]," " ,left_hip[1])
                if(left_foot_index[1] >left_knee[1] and left_knee[1] >left_hip[1]and  stick_lock==0 )or( right_foot_index[1] >right_knee[1] and right_knee[1] >right_hip[1]and stick_lock==0):
                    
                        if (stick_lefthand_elbow_angle<110 and stick_lefthand_elbow_angle>70 and stick_lock==0) or (stick_righthand_elbow_angle<110 and stick_righthand_elbow_angle>70 and stick_lock==0) :#預備動作
                            
                            if (abs(left_shoulder[0]-left_elbow[0])<abs(left_foot_index[1]-left_heel[1]) and stick_lock==0) or (abs(right_shoulder[0]-right_elbow[0])<abs(right_foot_index[1]-right_heel[1]) and stick_lock==0):   
                                
                                if (stick_lefthand_balance_angle>20  and  stick_lefthand_balance_angle<60 and stick_lock==0) or (stick_righthand_balance_angle>20 and stick_righthand_balance_angle<60 and stick_lock==0)  :#肩膀與腳趾與地板的角度#防站著
                                    
                                    if (stick_lefthand_knee_angle>160 and stick_lock==0) or (stick_righthand_knee_angle>160 and stick_lock==0):#預備動作
                                        
                                        stick_lock=1
                                        print("4")
                                        stick_start = time.time()
                                        stick_stage = "good"
                                        Thread(speak("很好請保持"))
                                    else:
                                        if stick_lock==0:
                                            Thread(speak("膝蓋請勿彎曲"))
                                else:
                                    if stick_lock==0:
                                        Thread(speak("請將身體抬起"))
                            else:
                                if stick_lock==0:
                                    Thread(speak("手肘請於肩膀正下方"))
                                
                        else:
                                if stick_lock==0:
                                    Thread(speak("手與肩膀請保持90度"))
                else:
                            if stick_lock==0:
                                Thread(speak("腳趾低於膝蓋低於臀部"))
                        
                
                
                if stick_stage =='good':
                    stick_end = time.time()
                        # Time elapsed
                    stick_seconds = stick_end - stick_start
                    print( "Time takenstick : {0} seconds".format(stick_seconds))
                    print("goal",your_goal_time)
                    if stick_seconds >= int(your_goal_time):
                        speak("成功")
                        counter_stick += int(your_goal_time)
                        print( "Time takenstick : {0} secondsysysysysy".format(stick_seconds))
                    else:
                        print("bad1") #wait 全島如何+ 膝蓋碰地yet
                        
                        #print("left_foot_index[1] <left_knee[1]",left_foot_index[1] ," ",left_knee[1] )
                        print("stick_lefthand_balance_angle_wrong",stick_lefthand_balance_angle_wrong)
                        if (stick_lefthand_balance_angle_wrong<=5   and  stick_stage =='good') or (stick_righthand_balance_angle_wrong<=5   and stick_stage =='good')or (stick_lefthand_balance_angle_wrong>=60  and  stick_stage =='good') or (stick_righthand_balance_angle_wrong>=60  and  stick_stage =='good'):#是否倒下 或站立 肩膀與腳踝與地板
                            speak("二錯")
                            print("bad2",countfault-1)
                            stick_end = time.time()
                                # Time elapsed
                            stick_seconds = stick_end - stick_start
                            countfault -=1
                            
                            if stick_seconds < int(your_goal_time) and countfault==0:
                                speak("失敗")
                                cap.release()#目前失敗關掉要改
                                cv2.destroyAllWindows()
                                
                            #print( "Time taken2 : {0} seconds".format(stick_seconds))
                        
                        if ( left_foot_index[1] <= left_knee[1] and stick_stage =='good') :#腳踝比膝蓋高or (right_foot_index[1]<=right_knee[1] and stick_stage =='good')
                            
                            speak("三錯")
                            print("bad3",countfault-1)
                            stick_end = time.time()
                                # Time elapsed
                            stick_seconds = stick_end - stick_start
                            countfault -=1
                            
                            if stick_seconds < int(your_goal_time) and countfault==0:
                                    speak("失敗")
                                    cap.release()#目前失敗關掉要改
                                    cv2.destroyAllWindows() 
                        if ( left_knee[1] <=left_hip[1] and stick_stage =='good') or (right_knee[1]<=right_hip[1] and stick_stage =='good'):#腳踝比膝蓋高
                            speak("四錯")
                            print("bad4",countfault-1)
                            stick_end = time.time()
                                # Time elapsed
                            stick_seconds = stick_end - stick_start
                            countfault -=1
                            print("bad4")
                            if stick_seconds < int(your_goal_time) and countfault==0:
                                    speak("失敗")
                                    cap.release()#目前失敗關掉要改
                                    cv2.destroyAllWindows() 
                        if (stick_lefthand_knee_angle<120 and stick_lock==0) or (stick_righthand_knee_angle<120 and stick_lock==0):
                            speak("五錯")
                            print("bad5",countfault-1)
                            stick_end = time.time()
                                # Time elapsed
                            stick_seconds = stick_end - stick_start
                            countfault -=1
                            print("bad5")
                            if stick_seconds < int(your_goal_time) and countfault==0:
                                    speak("失敗")
                                    cap.release()#目前失敗關掉要改
                                    cv2.destroyAllWindows() 
                    
                    
                    
                
    
            
                
            
                
        except:
            pass
        #print("hello")
        # Render curl counter
        # Setup status box
        cv2.rectangle(image, (0,0), (225,73), (245,117,16), -1)
        if action=="toss":
            # Rep data
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            # Stage data
            cv2.putText(image, 'STAGE', (65,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (60,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                        

        if action=="serve":
           
            # Rep data
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter_serve), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            
            # Stage data
            cv2.putText(image, 'STAGE', (65,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, serve_stage, 
                        (60,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        if action=="深蹲":
           
            # Rep data
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter_squat), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            
            # Stage data
            cv2.putText(image, 'STAGE', (65,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, squat_stage, 
                        (60,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        if action=="仰臥起坐":
           
            # Rep data
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter_situp), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            
            # Stage data
            cv2.putText(image, 'STAGE', (65,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, situp_stage, 
                        (60,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        if action=="棒式":
           
            # Rep data
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter_stick), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            
            # Stage data
            cv2.putText(image, 'STAGE', (65,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stick_stage, 
                        (60,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    


struct_time = time.localtime() 
timeString = time.strftime("%Y-%m-%d ", struct_time)
timeString=timeString+" 00:00:00"
struct_time_lastrecord = time.strptime(timeString, "%Y-%m-%d %H:%M:%S") # 轉成時間元組
time_stamp_today = int(time.mktime(struct_time_lastrecord)) # 轉成時間戳
print(time_stamp_today)

create= open("timestamp.txt", "a+")
create.close()
create_no_makeup= open("timestamp_file_no_makeup.txt", "a+")
create_no_makeup.close()

#how many day are empty
day_empty= open("timestamp.txt", "r")
size = os.path.getsize('timestamp.txt') 
if size == 0:
    print('文件是空的')
else:
    print('文件不是空的')
    lines=day_empty.readlines()
    dataset = json.loads(lines[-1])
    timeString=dataset['time'][0:10]+" 00:00:00"
    
    struct_time_lastrecord = time.strptime(timeString, "%Y-%m-%d %H:%M:%S") # 轉成時間元組
    time_stamp_lastrecord = int(time.mktime(struct_time_lastrecord)) # 轉成時間戳
    print(time_stamp_lastrecord)
    day=math.ceil((time_stamp_today-time_stamp_lastrecord)/86400)#how many day
    day_empty.close()
    
    #Make_up_time
    Make_up_time = open("timestamp.txt", "a+")
    No_Make_up_time = open("timestamp.txt", "a+")
    data=dict()
    action=dict()
    for i in range(day-1):
        add_record=time_stamp_lastrecord+86400*(i+1)
        print(add_record)
        struct_time_add = time.localtime(add_record) # 轉成時間元組
        add_record = time.strftime("%Y-%m-%d %H:%M:%S", struct_time_add) # 轉成字串
        action={'toss':counter,'serve':counter_serve,'squat':counter_squat,'situp':counter_situp,'stick':int(counter_stick)}#棒式以10為一個單位
        data['time']=add_record.replace('/n','')
        data['action']=action
        Make_up_time.write(str(json.dumps(data)+'\n'))              
    Make_up_time.close()



#save new one
file1 = open("timestamp.txt", "a+")
file_no_makeup = open("timestamp_file_no_makeup.txt", "a+")
print("file1")
t = time.localtime()
time = time.strftime("%Y%m%d %H:%M:%S", t)

action={'toss':counter,'serve':counter_serve,'squat':counter_squat,'situp':counter_situp,'stick':int(counter_stick)}#棒式以10為一個單位
data['time']=time.replace('/n','')
data['action']=action
file1.write(json.dumps(data)+'\n')

no_makeup_data['time']=time
no_makeup_data['action']=action
file_no_makeup.write(json.dumps(no_makeup_data)+'\n')

file1.close()
file_no_makeup.close()




