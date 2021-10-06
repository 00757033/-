# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 13:54:51 2021
@author: lspss
"""
def dive():
  import numpy as np
  import mediapipe as mp
  import cv2
  import random
  img1 = cv2.imread('volleyball_pic2.png')
  width = int(img1.shape[1] * 70 / 705) # 縮放後圖片寬度
  height = int(img1.shape[0] * 70 / 706) # 縮放後圖片高度
  dim = (width, height) # 圖片形狀 
  img1 = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)
  rows, cols= img1.shape[:2]
  print("rows,cols",rows,cols)  
  mp_drawing = mp.solutions.drawing_utils
  mp_pose = mp.solutions.holistic
  video_name = 'video08228_'
  file_type = '.avi'
  _CAMERA_WIDTH = 640
  _CAMERA_HEIGH = 480
  prwrite_flag = 0
  video_counter = 0
  newx = 0
  fourcc = cv2.VideoWriter_fourcc(*'XVID')
  FPS = 20
  cap = cv2.VideoCapture(0) #cv2.CAP_V4L2
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, _CAMERA_WIDTH)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, _CAMERA_HEIGH)
  #x = 400#random.randint(10,400)
  #y = 200#random.randint(10,440)
  #print("x,y",x,y)
  def resize_img(img, scale_percent):

        width = int(img.shape[1] * scale_percent / 100) # 縮放後圖片寬度
        height = int(img.shape[0] * scale_percent / 100) # 縮放後圖片高度
        dim = (width, height) # 圖片形狀 
        resize_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)  
    
        return resize_img
    
  def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle

  #img = resize_img(img,20)
  #h, w = img.shape[:2] 
  cnt = 0  
  with mp_pose.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

    touched = 0
    score = 0
    x=0
    y=0
    good = 0    # 低手姿勢
    ball = 0
    ending_count = 0
    #out2 = cv2.VideoWriter(video_name+'0', fourcc, FPS, (_CAMERA_WIDTH, _CAMERA_HEIGH))
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
              print("Can't receive frame (stream end?). Exiting ...")
              break

        frame = cv2.flip(frame,1)
        
        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Make Detections
        results = holistic.process(image)
        #image = cv2.flip(image,1)

        try:
            cnt+=1
            #print('cnt',cnt)
            
            landmarks = results.pose_landmarks.landmark
            nose = [landmarks[0].x,landmarks[0].y,landmarks[0].z]
            left_ear = [landmarks[8].x,landmarks[8].y,landmarks[8].z]
            right_ear = [landmarks[7].x,landmarks[7].y,landmarks[7].z]
            left_shoulder = [landmarks[12].x,landmarks[12].y,landmarks[12].z]
            right_shoulder= [landmarks[11].x,landmarks[11].y,landmarks[11].z]
            left_elbow= [landmarks[14].x,landmarks[14].y,landmarks[14].z]
            right_elbow= [landmarks[13].x,landmarks[13].y,landmarks[13].z]
            left_wrist=[landmarks[16].x,landmarks[16].y,landmarks[16].z]
            right_wrist=[landmarks[15].x,landmarks[15].y,landmarks[15].z]
            
            right_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            right_index = [landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y]
            right_heel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
            right_foot_index = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
            
            left_heel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
            left_foot_index = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
            left_index = [landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            left_thumb = [landmarks[mp_pose.PoseLandmark.RIGHT_THUMB.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_THUMB.value].y]
            right_thumb = [landmarks[mp_pose.PoseLandmark.LEFT_THUMB.value].x,landmarks[mp_pose.PoseLandmark.LEFT_THUMB.value].y]
            
            #print("left_wrist",left_wrist)
            #print("right_wrist",right_wrist)
            #print("left_hand_landmarks",left_hand_landmarks)
            #drawing_spec1=mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
            
            # Recolor image back to BGR for rendering
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            #cv2.putText(image, img, (15, 15))
            #cv2.line(image, (0, 0), (640, 480), (0, 0, 255), 5)
            
            mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
            
           # print("left_wrist",left_wrist)
            rows,cols = img1.shape[:2]
            
            if cnt == 30 :
                #x = 1#random.randint(1,400)
                y = random.randint(1,600)
                newx = 1
                #print("new",newx,y)
            if  touched >0 : 
                newx-=10 
            elif touched==0 : 
                newx+=10
                #print("newx", newx)
            #print(newx,newx,cnt)    
            pixelL = mp_drawing._normalized_to_pixel_coordinates(left_wrist[0], left_wrist[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
            pixelR = mp_drawing._normalized_to_pixel_coordinates(right_wrist[0], right_wrist[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
            noseNormalize = mp_drawing._normalized_to_pixel_coordinates(nose[0], nose[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
            
            #finger
            pixelL_thumb = mp_drawing._normalized_to_pixel_coordinates(left_thumb[0], left_thumb[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
            pixelR_thumb = mp_drawing._normalized_to_pixel_coordinates(right_thumb[0], right_thumb[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
            
            # hand
            pixelL_shoulder = mp_drawing._normalized_to_pixel_coordinates(left_shoulder[0], left_shoulder[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
            pixelL_elbow = mp_drawing._normalized_to_pixel_coordinates(left_elbow[0], left_elbow[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
            pixelL_wrist = mp_drawing._normalized_to_pixel_coordinates(left_wrist[0], left_wrist[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
            
            pixelR_shoulder = mp_drawing._normalized_to_pixel_coordinates(right_shoulder[0], right_shoulder[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
            pixelR_elbow = mp_drawing._normalized_to_pixel_coordinates(right_elbow[0], right_elbow[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
            pixelR_wrist = mp_drawing._normalized_to_pixel_coordinates(right_wrist[0], right_wrist[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
            
            # leg
            pixelL_hip = mp_drawing._normalized_to_pixel_coordinates(left_hip[0], left_hip[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
            pixelL_knee = mp_drawing._normalized_to_pixel_coordinates(left_knee[0], left_knee[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
            pixelL_ankle = mp_drawing._normalized_to_pixel_coordinates(left_ankle[0], left_ankle[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
            
            pixelR_hip = mp_drawing._normalized_to_pixel_coordinates(right_hip[0], right_hip[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
            pixelR_knee = mp_drawing._normalized_to_pixel_coordinates(right_knee[0], right_knee[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
            pixelR_ankle = mp_drawing._normalized_to_pixel_coordinates(right_ankle[0], right_ankle[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
            
            angleL_hand = calculate_angle(pixelL_shoulder, pixelL_elbow, pixelL_wrist)
            angleR_hand = calculate_angle(pixelR_shoulder, pixelR_elbow, pixelR_wrist)
            
            angleL_leg = calculate_angle(pixelL_hip, pixelL_knee, pixelL_ankle)
            angleR_leg = calculate_angle(pixelR_hip, pixelR_knee, pixelR_ankle)
            
 
            '''
            if y < 680//2 and cnt >= 30 :
                #pixelL = mp_drawing._normalized_to_pixel_coordinates(left_wrist[0], left_wrist[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
                pixel=pixelL
                print('left hand')
                cv2.putText(image, 'left hand', (10, 120), cv2.FONT_HERSHEY_DUPLEX,2, (0, 255, 255), 1, cv2.LINE_AA)
            elif cnt >= 30 :
                #pixelR = mp_drawing._normalized_to_pixel_coordinates(right_wrist[0], right_wrist[1], _CAMERA_WIDTH, _CAMERA_HEIGH)
                pixel=pixelR
                print('right hand')
                cv2.putText(image, 'right hand', (10, 120), cv2.FONT_HERSHEY_DUPLEX,2, (0, 255, 255), 1, cv2.LINE_AA)
               
            if pixelL_thumb:
                print("L",pixelL_thumb[0],pixelL_thumb[1])
            if pixelR_thumb:
                print("R",pixelR_thumb[0],pixelR_thumb[1])
            '''
                
            if abs(pixelL_thumb[0]-pixelR_thumb[0]) < 15 and abs(pixelL_thumb[1]-pixelR_thumb[1]) < 15 and angleL_hand > 160 and angleR_hand > 160 and angleL_leg > 140 and angleR_leg > 140:
                good = 1
                #print("good")
                #print("angleL_hand", angleL_hand)
                #print("angleR_hand", angleR_hand)
                #print("angleL_leg", angleL_leg)
                #print("angleR_leg", angleR_leg)
                #cv2.putText(image, 'good', (10, 120), cv2.FONT_HERSHEY_DUPLEX,2, (0, 0, 0), 1, cv2.LINE_AA)
                
            if ( ((pixelL and pixelR and left_knee) and good == 0  and ( (pixelL[1]>=newx and pixelL[1]<=newx+(rows) and pixelL[0] >= y and pixelL[0] <= y+(cols)) or (pixelR[1]>=newx and pixelR[1]<=newx+(rows) and pixelR[0] >= y and pixelR[0] <= y+(cols)) ) and (noseNormalize[1] > 400*4//5)) or (good and pixelL_thumb[1]>=newx and pixelL_thumb[1]<=newx+(rows) and pixelL_thumb[0] >= y and pixelL_thumb[0] <= y+(cols) and (noseNormalize[1] <= 400*4//5 and noseNormalize[1] > 400*1//5)) ) and cnt >= 30 and touched==0  :
                touched+=1
                score+=1
                #print("score",score)
                cv2.putText(image, '+1' , (200, 250), cv2.FONT_HERSHEY_DUPLEX,2.5, (0, 255, 255), 1, cv2.LINE_AA)
            
            
            if  touched >=1 and touched < 5 :
                touched+=1
                cv2.putText(image, '+1', (200, 250), cv2.FONT_HERSHEY_DUPLEX,2.5, (0, 255, 255), 1, cv2.LINE_AA)
            
            
            if  newx > 0 and newx < 400 and cnt >= 30: #cnt > 30 and cnt < 100  and
                rows,cols = img1.shape[:2]
                roi = image[newx:newx+rows,y:y+cols ]
                # Now create a mask of logo and create its inverse mask also
                img1gray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
                ret, mask = cv2.threshold(img1gray, 200, 255, cv2.THRESH_BINARY)
                mask_inv = cv2.bitwise_not(mask)
                img_bg = cv2.bitwise_and(roi,roi,mask = mask)
                # Take only region of logo from logo image.
                img1_fg = cv2.bitwise_and(img1,img1,mask = mask_inv)
                # Put logo in ROI and modify the main image
                dst = cv2.add(img_bg,img1_fg)
                
                image[newx:newx+rows,y:y+cols ] = dst
                #print("ball",newx,newx+rows,y,y+cols)
                
                #v2.circle(image,(y, x), 15, (255, 0, 0), -1)
                #cv2.circle(image,(y+(70), x), 15, (255, 0, 0), -1)
                #cv2.circle(image,(y, x+(70)), 15, (255, 0, 0), -1)
                #cv2.circle(image,(y+(70), x+(70)), 15, (255, 0, 0), -1)
            elif cnt > 30:
                cnt = 0
                touched = 0
                newx = 0
                good=0
                ball +=1
                print("score",score)
    
            cv2.rectangle(image, (10, 10), (260, 75), (0, 0, 0), -1)
            cv2.putText(image, f'Score: {score}', (20, 55), cv2.FONT_HERSHEY_DUPLEX,1.5, (0, 255, 255), 1, cv2.LINE_AA)
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            #cv2.imshow('S.S.A', img1)
            
            '''
            # Draw face landmarks
            mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
            
            # Right hand
            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    
            # Left Hand
            mp_drawing.draw_landmarks(image, results.left_hand_landqmarks, mp_holistic.HAND_CONNECTIONS)
    
            # Pose Detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
            '''      
            # ending
            if abs(pixelL_thumb[0]-pixelR_thumb[0]) < 40 and abs(pixelL_thumb[1]-pixelR_thumb[1]) < 15 and angleL_hand > 90 and angleR_hand > 90 and pixelL_thumb[1] < noseNormalize[1]-50 and score > 0 and ball > 0:
                cv2.putText(image, 'finished :)' , (200, 250), cv2.FONT_HERSHEY_DUPLEX,1.5, (0, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(image, f'You get {score} out of {ball}.  {round(score*100/ball)}%' , (25, 300), cv2.FONT_HERSHEY_DUPLEX,1.25, (0, 255, 255), 1, cv2.LINE_AA)
                ending_count += 1
            if ending_count >= 1 and ending_count <= 100:
                ending_count += 1
                print(ending_count)
            elif ending_count > 100:
                print(":) ", ending_count)
                break
            
        except:
            
            pass
        cv2.imshow('SSA', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            #out2.release()
            break
        
    #out2.release()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__': 
  dive()