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

@author: 翁培馨
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 22:00:42 2021

@author:"""

def training(text,goaltime):
        
    
    # voice
    
    try:
        
        import time
        import cv2
        import datetime
        from tkinter import messagebox
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
       		#print("123")
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
        action=text#input("請輸入動作action:toss serve 深蹲 仰臥起坐")
        print(action,goaltime)
        #print(round(int(goaltime/10)10))
        if action=="stick":
            your_goal_time=goaltime#input("請輸入棒式的時間")
            print(round(int(your_goal_time)/10))
            countfault=int(your_goal_time)/5
            break
        if action=="toss" or action=="serve" or action=="squat" or action=="situp":
            break
        
        
    
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    cap =  cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')    
    loc_dt = datetime.today()

    day = loc_dt.strftime('%Y-%m-%d %H-%M-%S')
    #print(day)
    aa = '2018-04-06 05-40-55'
    videoName = 'video/'+ action + '_' + aa + '.avi'
    #print(videoName)

    #MsgBox = messagebox.askquestion ('Alert','Do you want to record?')
    #if MsgBox == 'yes':
    #    out = cv2.VideoWriter(videoName, fourcc, 20.0, (640,  480))
    
    # Curl counter variables
    count321=0
    start0 = time.time()
    close0=0
    close1=0
    close2=0
    close3=0
    close4=0
    close5=0
    counter = 0 
    counter_serve = 0 
    counter_squat = 0 
    counter_situp = 0 
    counter_stick=0
    count_cross=0
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
                    cv2.putText(image, str("Please take the whole body "), 
                               tuple(np.multiply([0.15,0.8], [640, 480]).astype(int)), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA
                                    )
                    cv2.putText(image, str("into the mirror"), 
                               tuple(np.multiply([0.25,0.9], [640, 480]).astype(int)), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA
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
                
                
                # Calculate angle squat
                
                squat_lefthand_hip_angle = calculate_angle( left_shoulder,left_hip,left_knee)#
                squat_righthand_hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)
                squat_lefthand_knee_angle = calculate_angle( left_hip,left_knee,left_ankle)#
                squat_righthand_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
                squat_righthand_body_angle = calculate_angle2(right_shoulder, right_hip, right_foot_index)#上半身過度前傾： 因為深蹲時重心向後移，人會下意識地往前傾來平衡，但正確姿勢建議肩膀、下背、臀部成一直線，並與地面夾50~70度，即使膝蓋因此稍微超過腳尖也沒關係。
                squat_leftthand_body_angle = calculate_angle2(left_shoulder,left_hip, left_foot_index)#上半身過度前傾： 因為深蹲時重心向後移，人會下意識地往前傾來平衡，但正確姿勢建議肩膀、下背、臀部成一直線，並與地面夾50~70度，即使膝蓋因此稍微超過腳尖也沒關係。
                squat_righthand_balance_angle = calculate_angle2(right_hip, right_knee, right_foot_index)#角度臀部 膝蓋 - 角度3032<20(要平行
                squat_lefthand_balance_angle = calculate_angle2(left_hip, left_knee, left_foot_index)#角度臀部 膝蓋 - 角度3032<20(要平行

                
                
                
                
                
                
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
                if seconds0>=1 and close5==0:
                    cv2.putText(image, str("5"), 
                       tuple(np.multiply([0.45,0.55], [640, 480]).astype(int)), 
                       cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 10, cv2.LINE_AA
                       )
                    speak("5")
                    close5=1
                if seconds0>=2 and close4==0:
                    cv2.putText(image, str("4"), 
                       tuple(np.multiply([0.45,0.55], [640, 480]).astype(int)), 
                       cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 10, cv2.LINE_AA
                       )   
                    speak("4")
                    close4=1
                 
                if seconds0>=3 and close3==0:
                    cv2.putText(image, str("3"), 
                       tuple(np.multiply([0.45,0.55], [640, 480]).astype(int)), 
                       cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 10, cv2.LINE_AA
                       ) 
                    speak("3")
                    close3=1
                   
                if seconds0>=4 and close2==0:
                    cv2.putText(image, str("2"), 
                       tuple(np.multiply([0.45,0.55], [640, 480]).astype(int)), 
                       cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 10, cv2.LINE_AA
                       )
                    speak("2")
                    close2=1
                    
                if seconds0>=5 and close1==0:
                    cv2.putText(image, str("1"), 
                       tuple(np.multiply([0.45,0.55], [640, 480]).astype(int)), 
                       cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 10, cv2.LINE_AA
                       )
                    speak("1")
                    close1=1
                if seconds0>=6 and close0==0:
                    close0=1
                    speak("start")
                    cv2.putText(image, str("start"), 
                       tuple(np.multiply([0.45,0.55], [640, 480]).astype(int)), 
                       cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 10, cv2.LINE_AA
                       )
                    count321=1
                if  check==0:
                    serve_stage = "wait"
                    situp_stage = "wait"
                    squat_stage = "wait"
                    stick_stage = "wait"
                    stage = "wait"
                if check==1 and count321==1 and abs(left_shoulder[0]-left_foot_index[0])<abs(left_shoulder[1]-left_foot_index[1]):
                   #print('left_elbow',left_elbow,'left_wrist',left_wrist)
                   #print('right_elbow',right_elbow,'right_wrist',right_wrist)
                   if left_elbow[0]<right_elbow[0] and left_wrist[0]>right_wrist[0] and left_wrist[1] > left_shoulder[1] and right_wrist[1] > right_shoulder[1] and toss_lefthand_elbow_angle<60:
                           print('count_cross',count_cross)
                           count_cross+=1
                           if count_cross==30:
                              print('end1')
                              speak('bye bye')
                              cap.release()
                              break
                              #cv2.destroyAllWindows()
                   elif left_elbow[0]>right_elbow[0] and left_wrist[0]<right_wrist[0]and left_wrist[1] > left_shoulder[1] and right_wrist[1] > right_shoulder[1] and toss_lefthand_elbow_angle<60:
                           print('count_cross',count_cross)
                           count_cross+=1
                           if count_cross==40:
                              print('end2')
                              speak('bye bye')
                              cap.release()
                              break
                              #cv2.destroyAllWindows()
                   else :
                      
                      count_cross=0
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
                        count=count-1
                    if toss_lefthand_elbow_angle > 160 and toss_lefthand_shoulder_angle > 160 and toss_righthand_elbow_angle > 160 and toss_righthand_shoulder_angle > 160 and toss_leftheight-heightl1>abs(left_hip[0]-right_hip[0])*20 and stage =='down':
                        stage="up"
                        counter +=1

                        first_time=1
                        cv2.putText(frame, "o", (200, 250), cv2.FONT_HERSHEY_DUPLEX,10, (0, 255, 255), 5, cv2.LINE_AA)
                        speak("success")
                    
    
                    # Curl counter logic
                if action=="serve"and check==1 and count321==1:
                    if serve_righthand_elbow_angle >130 and serve_lefthand_shoulder_angle >80 and serve_righthand_higherthan_ear<0 and serve_lefthand_higherthan_ear>0 and count <0:#預備動作
                        #
                        print("step1/2")
                        #print(count)
                        serve_stage = "step1/3"
        
                    if serve_righthand_higherthan_ear>0   and serve_righthand_elbow_angle >140 and serve_lefthand_higherthan_ear>0   and serve_stage =='step1/3':#拋球 兩手皆要超過耳朵
                        count=40
                        serve_stage="step2/3"
                        print("step2/2")
                        print(count)
        
                    if  serve_lefthand_higherthan_ear<0  and serve_lefthand_elbow_angle >140  and serve_stage =='step2/3':
                        serve_stage="step3/3"
                        counter_serve +=1
                        cv2.putText(frame, "o", (200, 250), cv2.FONT_HERSHEY_DUPLEX,10, (0, 255, 255), 5, cv2.LINE_AA)
                        speak("success")
                        count=-1
                        #print("step3")
                        #print(counter_serve)
                    if serve_stage =='step2/3' or serve_stage =='step3/3':
                        count=count-1
                    
                    
                    
                    
                if action=="squat"and check==1 and (left_knee[1]<1 and left_knee[1]>0)  and (left_hip[1]<1 and left_hip[1]>0) and (left_shoulder[1]<1 and left_shoulder[1]>0) and count321==1:

            
                    if left_foot_index[0]>left_heel[0] and squat_stage !='step1':#面向螢幕右邊 
                        if left_knee[0]>left_foot_index[0]+(left_foot_index[0]-left_heel[0])/4:
                            Thread(speak("Please do not exceed your knees above your toes Please try again"))
                            squat_stage = "step1"
                            
                    if right_foot_index[0]<right_heel[0]and squat_stage !='step1':
                        #print("474",right_foot_index[0],right_heel[0],(right_foot_index[0]-right_heel[0])/2)
                        #print("475",right_knee[0],right_foot_index[0],(right_foot_index[0]-right_heel[0])/2)
                        if right_knee[0]<right_foot_index[0]-(right_heel[0]-right_foot_index[0])/2:
                            Thread(speak("Please do not exceed your knees above your toes Please try again"))
                            squat_stage = "step1"
                    if (squat_lefthand_knee_angle <180 and squat_lefthand_knee_angle >=160 and lock==0) or (squat_righthand_knee_angle <180 and squat_righthand_knee_angle >=160 and lock==0):
                        start = time.time()
                        save=0
                        lock=0
                        
                        squat_stage = "step1"
                    if (squat_lefthand_knee_angle <160 and squat_lefthand_knee_angle >=150 and lock==0 and squat_stage !='step3'and squat_stage =='step1') or (squat_righthand_knee_angle <160 and squat_righthand_knee_angle >=150 and lock==0 and squat_stage !='step3'and squat_stage =='step1') :
                        
                        squat_stage = "step2"
                        
        
                    if (squat_lefthand_knee_angle <90 and squat_lefthand_knee_angle > 40 and lock==0  and squat_stage =='step2')or (squat_righthand_knee_angle<90 and squat_righthand_knee_angle>40 and lock==0  and squat_stage =='step2') :
                        if (left_foot_index[1]-left_heel[1]<abs(left_foot_index[0]-left_heel[0])/2)or (right_foot_index[1]-right_heel[1]<abs(right_foot_index[0]-right_heel[0])/2):
                            
                            end = time.time()
                            # Time elapsed
                            seconds = end - start 
                           # print( "Time taken1 : {0} seconds".format(seconds))
                            if seconds<0.5:
                                speak("You're doing too fast. Please try again.")
                                squat_stage = "step1"
                            #print("step3-1")
                            if (squat_righthand_body_angle >40 and squat_righthand_body_angle <80 and squat_stage !='step1' and lock==0) or(squat_leftthand_body_angle >40 and squat_leftthand_body_angle <80 and squat_stage !='step1' and lock==0) :
                                if abs(squat_lefthand_hip_angle - squat_lefthand_knee_angle<20 and lock==0)or (abs(squat_righthand_hip_angle - squat_righthand_knee_angle)<20 and lock==0):
                                    if (left_foot_index[1]-left_heel[1]<abs(left_foot_index[0]-left_heel[0])/2 and lock==0)or (right_foot_index[1]-right_heel[1]<abs(right_foot_index[0]-right_heel[0])/2 and lock==0):
                                       
                                        
                                       squat_stage="good"
                                       #print("step3-2")
                                                                              
                                       lock=1
                                       #print(lock)
        
                                    else:
                                        speak("Do not lift the back heel")
                                else:
                                    speak("The back is as parallel to the calf as possible ")
                            
                            else:
                                speak("The angle between the back and the floor must be between 50-80")
                        else:
                            squat_stage = "step1"
                            speak("Do not lift the back heel. Please try again.")
                        
                    if (squat_righthand_body_angle >50 and squat_righthand_body_angle <60 and lock==1) or(squat_leftthand_body_angle >50 and squat_leftthand_body_angle <80 and lock==1):
                        #speak("到了")
                        start2 = time.time()
                        #print("504",start2)
                        #print("start2",start2)
                    if (squat_lefthand_knee_angle <180 and squat_lefthand_knee_angle >=170 and lock==1 and squat_stage =='good') or (squat_righthand_knee_angle <180 and squat_righthand_knee_angle >=170 and lock==1 and squat_stage =='good') :#or (squat_righthand_knee_angle <180 and squat_righthand_knee_angle >=160))
                        lock=0
                        if (left_foot_index[1]-left_heel[1]<abs(left_foot_index[0]-left_heel[0])/2)or (right_foot_index[1]-right_heel[1]<abs(right_foot_index[0]-right_heel[0])/2):
                            end2 = time.time()
                            # Time elapsed
                            seconds2 = end2 - start2
                            #print("end2",end2)
                            #print( "Time taken2 : {0} seconds".format(seconds2))

                            #print("step4")
                            count=5
                            count2=0
                            squat_stage = "step4"
                            #print(lock)
                            if save==0 :
                               save=1
                               counter_squat=counter_squat+1
                               cv2.putText(frame, "o", (200, 250), cv2.FONT_HERSHEY_DUPLEX,10, (0, 255, 255), 5, cv2.LINE_AA)
                               speak("success")
                               #Thread(speak("次完成"))
                            
                        else:
                            Thread(speak("Do not lift the back heel. Please try again."))
                            squat_stage = "step1" 
                                                              
                        
                            
                    
    
                
                
                if action=="situp"and check==1 and (left_knee[1]<1 and left_knee[1]>0)  and (left_hip[1]<1 and left_hip[1]>0) and (left_shoulder[1]<1 and left_shoulder[1]>0) and count321==1:
                    #print("situp_lefthand_hip_angle",situp_lefthand_hip_angle)
                    #print("situp_lefthand_knee_angle",situp_lefthand_knee_angle)
                    if (situp_lefthand_knee_angle<100 and situp_lefthand_hip_angle<5) or (situp_righthand_knee_angle<100 and situp_righthand_hip_angle<5):#預備動作
                        lock_situp=1
                        #print("step1")
                        situp_stage = "down"
                        
                    
        
                    if (situp_lefthand_knee_angle<100 and situp_lefthand_hip_angle>20) or (situp_righthand_knee_angle<100 and situp_righthand_hip_angle>20) and situp_stage != "wait"and situp_stage =='down':#預備動作
                        if lock_situp==1:
                            cv2.putText(frame, "o", (200, 250), cv2.FONT_HERSHEY_DUPLEX,10, (0, 255, 255), 5, cv2.LINE_AA)
                            speak("success")
                            counter_situp=counter_situp+1
                            lock_situp=0
                            
                        
                        situp_stage = "up"
                        #print(situp_stage)
                        #print(situp_lefthand_hip_angle)
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        
                    
                if action=="stick"and check==1 and (left_knee[1]<1 and left_knee[1]>0)  and (left_hip[1]<1 and left_hip[1]>0) and (left_shoulder[1]<1 and left_shoulder[1]>0)  and count321==1:
                    #print("left_shoulder,left_foot_index",left_shoulder[1]," ",left_foot_index[1]," , ",left_shoulder[0]," ",left_foot_index[0])
                    #print("stick_lefthand_balance_angle",stick_lefthand_balance_angle)
                    #print("stick_lefthand_elbow_angle",stick_lefthand_elbow_angle)
                    #print("abs(left_shoulder[0]-left_elbow[0])<abs(left_foot_index[1]-left_heel[1])",abs(left_shoulder[0]-left_elbow[0]),"  ",abs(left_foot_index[1]-left_heel[1]))
                    #print("left_foot_index[1] >left_knee[1] and left_knee[1] >left_hip[1]",left_foot_index[1] ," ",left_knee[1]," " ,left_hip[1])
                    if(left_foot_index[1] >left_knee[1] and left_knee[1] >left_hip[1]and  stick_lock==0 )or( right_foot_index[1] >right_knee[1] and right_knee[1] >right_hip[1]and stick_lock==0 and ((left_hip[1]-left_shoulder[1])< math.sqrt(abs(left_foot_index[1]-left_heel[1])**2+abs(left_foot_index[0]-left_heel[0])**2)/2)):
                        
                            if (stick_lefthand_elbow_angle<130 and stick_lefthand_elbow_angle>50 and stick_lock==0) or (stick_righthand_elbow_angle<130 and stick_righthand_elbow_angle>50 and stick_lock==0) :#預備動作
                                
                                if (abs(left_shoulder[0]-left_elbow[0])<abs(left_foot_index[1]-left_heel[1]) and stick_lock==0) or (abs(right_shoulder[0]-right_elbow[0])<abs(right_foot_index[1]-right_heel[1]) and stick_lock==0):   
                                    
                                    if abs(left_shoulder[0]-left_foot_index[0])>abs(left_shoulder[1]-left_foot_index[1]):
                                        
                                        if (stick_lefthand_knee_angle>160 and stick_lock==0) or (stick_righthand_knee_angle>160 and stick_lock==0):#預備動作
                                            
                                            stick_lock=1
                                            #print("4")
                                            stick_start = time.time()
                                            stick_stage = "good"
                                            speak("Very good please keep")
                                        else:
                                            if stick_lock==0:
                                                Thread(speak("Do not bend your knees"))
                                    else:
                                        if stick_lock==0:
                                            Thread(speak("Please lift your body up"))
                                            #print(':):)')
                                else:
                                    if stick_lock==0:
                                        Thread(speak("Please place your elbows directly under your shoulders"))
                                    
                            else:
                                    if stick_lock==0:
                                        print('stick_lefthand_elbow_angle',stick_lefthand_elbow_angle)
                                        Thread(speak("Keep your hands and shoulders at 90 degrees"))
                    else:
                                if stick_lock==0:
                                    Thread(speak("Please lift your body up"))
                                    print(':)')
                                    continue
                            
                    
                    
                    if stick_stage =='good':
                        print("684")
                        stick_end = time.time()
                            # Time elapsed
                        stick_seconds = stick_end - stick_start
                        #print( "Time takenstick : {0} seconds".format(stick_seconds))
                        #print("goal",your_goal_time)
                        if stick_seconds >= int(your_goal_time):
                            cv2.putText(frame, "o", (200, 250), cv2.FONT_HERSHEY_DUPLEX,10, (0, 255, 255), 5, cv2.LINE_AA)
                            speak("success")
                            counter_stick += round(int(your_goal_time)/10)
                            #print( "Time takenstick : {0} secondsysysysysy".format(stick_seconds))
                            cap.release()#目前失敗關掉要改
                            #cv2.destroyAllWindows() 
                            break
                        else:
                            #print("bad1") #wait 全島如何+ 膝蓋碰地yet
                            
                            #print("left_foot_index[1] <left_knee[1]",left_foot_index[1] ," ",left_knee[1] )
                            #print("stick_lefthand_balance_angle_wrong",stick_lefthand_balance_angle_wrong)
                            #print("bad",stick_lefthand_balance_angle_wrong)
                            if  (stick_righthand_balance_angle_wrong<=5   and stick_stage =='good')or (abs(left_shoulder[0]-left_foot_index[0])<abs(left_shoulder[1]-left_foot_index[1])  and  stick_stage =='good') or (abs(left_shoulder[0]-left_foot_index[0])<abs(left_shoulder[1]-left_foot_index[1])  and  stick_stage =='good'):#是否倒下 或站立 肩膀與腳踝與地板
                                speak("come on")
                                print("bad2",stick_stage,abs(left_shoulder[0]-left_foot_index[0]),abs(left_shoulder[1]-left_foot_index[1]))
                                stick_end = time.time()
                                    # Time elapsed
                                stick_seconds = stick_end - stick_start
                                countfault -=1
                                
                                if stick_seconds < int(your_goal_time) and countfault<=0:
                                    speak("fail")
                                    cap.release()#目前失敗關掉要改
                                    
                                    break
                        
                                #print( "Time taken2 : {0} seconds".format(stick_seconds))
                            
                            if ( left_foot_index[1] <= left_knee[1]+(math.sqrt(abs(left_foot_index[1]-left_heel[1])**2+abs(left_foot_index[0]-left_heel[0])**2)/2) and stick_stage =='good') :#腳踝比膝蓋高or (right_foot_index[1]<=right_knee[1] and stick_stage =='good')
                                
                                speak("come on")
                                print("bad3",stick_stage,left_foot_index[1],left_knee[1])
                                stick_end = time.time()
                                    # Time elapsed
                                stick_seconds = stick_end - stick_start
                                countfault -=1
                                
                                if stick_seconds < int(your_goal_time) and countfault<=0:
                                        speak("fail")
                                        cap.release()#目前失敗關掉要改
                                        break
                        
                            if ((left_hip[1]-left_shoulder[1])> math.sqrt(abs(left_foot_index[1]-left_heel[1])**2+abs(left_foot_index[0]-left_heel[0])**2)) and stick_stage =='good':#腳踝比膝蓋高
                                speak("come on")
                                print("bad4",(left_hip[1]-left_shoulder[1]),math.sqrt(abs(left_foot_index[1]-left_heel[1])**2+abs(left_foot_index[0]-left_heel[0])**2)/2)
                                stick_end = time.time()
                                    # Time elapsed
                                stick_seconds = stick_end - stick_start
                                countfault -=1
                                #print("bad4")
                                if stick_seconds < int(your_goal_time) and countfault<=0:
                                        speak("fail")
                                        cap.release()#目前失敗關掉要改
                                        break
                        
                            if (stick_lefthand_knee_angle<120 and stick_lock==0) or (stick_righthand_knee_angle<120 and stick_lock==0):
                                speak("come on")
                                print("bad5",stick_stage)
                                stick_end = time.time()
                                    # Time elapsed
                                stick_seconds = stick_end - stick_start
                                countfault -=1
                                #print("bad5")
                                if stick_seconds < int(your_goal_time) and countfault<=0:
                                        speak("fail")
                                        cap.release()#目前失敗關掉要改
                                        break
                        
                        
                        
                    
        
                
                    
                
                    
            except:
                pass
            #print("hello")
            # Render curl counter
            # Setup status box
            cv2.rectangle(image, (0,0), (250,73), (132,141,129), -1)
            if action=="toss":
                # Rep data

                cv2.putText(image, str(counter), 
                            (10,60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 2, cv2.LINE_AA)
                

                cv2.putText(image, stage, 
                            (60,60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
                          
    
            if action=="serve":
               
                # Rep data
                
                cv2.putText(image, str(counter_serve), 
                            (10,60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 2, cv2.LINE_AA)
                
 
                cv2.putText(image, serve_stage, 
                            (55,60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                
            if action=="squat":
               

                cv2.putText(image, str(counter_squat), 
                            (10,60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 2, cv2.LINE_AA)
                
                
                if squat_stage=='good':
                    
                    cv2.putText(image, squat_stage, 
                                (55,60), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                
            if action=="situp":
               

                cv2.putText(image, str(counter_situp), 
                            (10,60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 2, cv2.LINE_AA)
                

                cv2.putText(image, situp_stage, 
                            (55,60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                
                    
            if action=="stick":
               
               

                if stick_stage=='good':
                    cv2.putText(image, str(int(stick_seconds)), 
                            (10,60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 3, (255,255,255), 2, cv2.LINE_AA)
                # Stage data
                
                    cv2.putText(image, stick_stage, 
                                (55,60), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                
            '''
            
            # Render detections 畫骨架
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                     )      
            '''
            #if MsgBox == 'yes':
            #    out.write(frame)
            cv2.imshow('S.S.A', image)
    
            if cv2.waitKey(10) & 0xFF == ord('q' or 'Q'):
                break
            
        cap.release()
        #if MsgBox == 'yes':
        #    out.release()
        cv2.destroyAllWindows()
        
    
    
    struct_time = time.localtime() 
    timeString = time.strftime("%Y-%m-%d ", struct_time)
    timeString=timeString+" 00:00:00"
    struct_time_lastrecord = time.strptime(timeString, "%Y-%m-%d %H:%M:%S") # 轉成時間元組
    time_stamp_today = int(time.mktime(struct_time_lastrecord)) # 轉成時間戳
    #print(time_stamp_today)
    
    create= open("Physical/timestamp.txt", "a+")
    create.close()

    
    #how many day are empty
    day_empty= open("Physical/timestamp.txt", "r")
    size = os.path.getsize('Physical/timestamp.txt') 
    if size == 0:
        print('文件是空的')
    else:
        #print('文件不是空的')
        lines=day_empty.readlines()
        #dataset = json.loads(lines[-1])

        base64_bytes = lines[-1].encode("ascii")
        sample_string_bytes = base64.b64decode(base64_bytes)
        sample_string = sample_string_bytes.decode("ascii")
        dataset = json.loads(sample_string)


        timeString=dataset['time'][0:10]+" 00:00:00"
        
        struct_time_lastrecord = time.strptime(timeString, "%Y-%m-%d %H:%M:%S") # 轉成時間元組
        time_stamp_lastrecord = int(time.mktime(struct_time_lastrecord)) # 轉成時間戳
        #print(time_stamp_lastrecord)
        day=math.ceil((time_stamp_today-time_stamp_lastrecord)/86400)#how many day
        day_empty.close()
        
        #Make_up_time
        Make_up_time = open("Physical/timestamp.txt", "a+")
        No_Make_up_time = open("Physical/timestamp.txt", "a+")
        data=dict()
        action=dict()
        for i in range(day-1):
            add_record=time_stamp_lastrecord+86400*(i+1)
            #print(add_record)
            struct_time_add = time.localtime(add_record) # 轉成時間元組
            add_record = time.strftime("%Y-%m-%d %H:%M:%S", struct_time_add) # 轉成字串
            action={'toss':int(0),'serve':int(0),'squat':int(0),'situp':int(0),'stick':int(0)}#棒式以10為一個單位
            data['time']=add_record
            data['action']=action
            #Make_up_time.write(str(json.dumps(data)+'\n'))
            message = str(json.dumps(data))
            message_bytes = message.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            base64_message = base64_bytes.decode('ascii')
            Make_up_time.write(base64_message+'\n')              
        Make_up_time.close()
    
    
    
 
    #save new one
    file1 = open("Physical/timestamp.txt", "a+")
    #file_no_makeup = open("timestamp_file_no_makeup.txt", "a+")
    
    t = time.localtime()
    time = time.strftime("%Y-%m-%d %H:%M:%S", t)
    
    action={'toss':counter,'serve':counter_serve,'squat':counter_squat,'situp':counter_situp,'stick':int(counter_stick)}#棒式以10為一個單位
    data['time']=time
    data['action']=action
    #file1.write(json.dumps(data)+'\n')

    message = str(json.dumps(data))
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    file1.write(base64_message+'\n')
    '''
    no_makeup_data['time']=time
    no_makeup_data['action']=action
    if  counter!=0 and counter_serve!=0 and counter_squat!=0 and counter_situp!=0 and int(counter_stick)!=0 :#棒式以10為一個單位
        file_no_makeup.write(json.dumps(no_makeup_data)+'\n')
    file_no_makeup.close()
    '''
    file1.close()
    print("file1")

    
    

