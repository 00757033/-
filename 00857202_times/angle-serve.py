# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 01:43:20 2021

@author: User
"""
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 22:00:42 2021

@author: 00857202
"""
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


data=dict()
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
action=input("請輸入action:toss serve ")

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)

# Curl counter variables
counter = 0 
counter_serve = 0 
stage = None
serve_stage = None
def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        
        
            
        ret, frame = cap.read()
        if ret==True:#水平翻轉
            frame = cv2.flip(frame,180)
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
            left_index = [landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            left_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            left_ear = [landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].y]
            
            # Calculate angle toss
            toss_lefthand_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
            toss_lefthand_shoulder_angle = calculate_angle( left_elbow,left_shoulder,left_hip)
            toss_righthand_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            toss_righthand_shoulder_angle = calculate_angle( right_elbow,right_shoulder,right_hip)
            
            if left_ankle[1]<1 and left_ankle[1]>0 and nose[1]<1 and nose[1]>0 and left_index[0]>0 and left_index[0]<1 and right_index[0]>0 and right_index[0]<1:
                toss_leftheight = abs(nose[1]-left_ankle[1])*100
                toss_rightheight =abs(nose[1]-right_ankle[1])*100
                check=1
                
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
            cv2.putText(image, str(serve_righthand_elbow_angle), 
                           tuple(np.multiply(right_elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA
                                )
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
            if  check==0:
               serve_stage = "wait"
               stage = "wait"
            if action=="toss" and check==1:
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
                print("toss",heightl1)    
                print("toss2",heightl1-toss_leftheight)
                print("hip",abs(left_hip[0]-right_hip[0])*100)
                if toss_lefthand_elbow_angle > 160 and toss_lefthand_shoulder_angle > 160 and toss_righthand_elbow_angle > 160 and toss_righthand_shoulder_angle > 160 and toss_leftheight-heightl1>abs(left_hip[0]-right_hip[0])*20 and stage =='down':
                    stage="up"
                    counter +=1
                    print(stage)
                    #print(abs(left_hip[0]-right_hip[0])*100)
                    #print(counter)
                    first_time=1
                

                # Curl counter logic
            if action=="serve"and check==1:
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
    data=dict()
    action=dict()
    for i in range(day-1):
        add_record=time_stamp_lastrecord+86400*(i+1)
        print(add_record)
        struct_time_add = time.localtime(add_record) # 轉成時間元組
        add_record = time.strftime("%Y-%m-%d %H:%M:%S", struct_time_add) # 轉成字串
        action={'toss':0,'serve':0}
        data['time']=add_record
        data['action']=action
        Make_up_time.write(str(json.dumps(data)+'\n'))              
    Make_up_time.close()

#save
file1 = open("timestamp.txt", "a+")
print("file1")
t = time.localtime()
time = time.strftime("%Y-%m-%d %H:%M:%S", t)

action={'toss':counter,'serve':counter_serve}
data['time']=time
data['action']=action
file1.write(json.dumps(data)+'\n')

file1.close()
