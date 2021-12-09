#lstm input  format
# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import time
import datetime
import numpy as np
import re
import copy
import tensorflow as tf
from tkinter import messagebox
video_name = 'video_'
file_type = '.avi'
_CAMERA_WIDTH = 640
_CAMERA_HEIGH = 480
prwrite_flag = 0
video_counter = 0
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
FPS = 20




def calculate_angle(a,b,c):#Clockwise
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])#radian
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
    return angle

def dect_loop(Right,records):
  print(Right)
  try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Windows Import
        if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '/../../../python/openpose/Release');
            os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
            import pyopenpose as op
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('../../../python');
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_dir", default="../../../examples/media/go.MP4", help="Process a directory of images. Read all standard formats (jpg, png, bmp, etc.).")
    parser.add_argument("--no_display", default=False, help="Enable to disable the visual display.")
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../../../models/"

    # Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1: next_item = args[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item

    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Read frames on directory
    #imagePaths = op.get_images_on_directory(args[0].image_dir);
    #imagePaths = cv2.VideoCapture(args[0].image_dir)
    # start = time.time()
    #fn = input('Enter file name: ')
    start = time.time()
    #path = '../../examples/media/video/serve/serve_bad_093004/serve_bad_093004'      #/serve_00857202
    #file = open(path+'_30.txt', 'a')
    #except IOError:
        #file = open(fn, 'w')
        # Process and display images
        #for imagePath in imagePaths:

    #video = cv2.VideoCapture(path+'.mp4') 
    pose = list()
    final = list()
    datum = op.Datum()
    video = cv2.VideoCapture(0)
    loc_dt = datetime.datetime.today()
    today_time = loc_dt.strftime('%Y-%m-%d %H-%M-%S')
    codec=cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    out2 = cv2.VideoWriter('Record/video/serve_'+today_time+'.mp4', codec, 20, (640, 480))
    img1 = cv2.imread('pic/volleyball_pic2.jpg')
    width = int(img1.shape[1] * 640 / 705) # 縮放後圖片寬度
    height = int(img1.shape[0] * 480 / 706) # 縮放後圖片高度
    dim = (width, height) # 圖片形狀 
    img1 = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)
    def classify(pose) :
               #print(len(pose))
               blocks = int(len(pose) / 30)
               print( blocks )   
               #print("here",type(pose),pose)
               #pose = np.array(np.split(pose,blocks))
               tf.compat.v1.reset_default_graph()
               with tf.compat.v1.Session() as sess:
                   new_saver = tf.compat.v1.train.import_meta_graph('lstm/serve/servelog1/serve_30_multiplayer.ckpt.meta')
                   new_saver.restore(sess,'lstm/serve/servelog1/serve_30_multiplayer.ckpt')
                   y = tf.compat.v1.get_collection('pred_network')
   
    
                   y=tf.argmax(y,2)+1
                   pose2=list()
                   pose2.append(pose)
                   #print(pose2)
                   #tf.compat.v1.reset_default_graph()
                   graph = tf.compat.v1.get_default_graph()
                   input_x = graph.get_operation_by_name('input_x').outputs[0]
                   keep_prob = graph.get_operation_by_name('keep_prob').outputs[0]
                   zz=sess.run(y, feed_dict={input_x:pose2,  keep_prob:1.0})[0]
                   #print(pose)
                   final.append(zz[0])
                   print("ZZ: ) ", zz)
                   if zz[0] ==1:
                      print("correct")
                      cv2.putText(frame, "o", (200, 250), cv2.FONT_HERSHEY_DUPLEX,10, (0, 255, 255), 5, cv2.LINE_AA)
                      cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData) 
                      #out2.write(img1) 
                      #index.jpeg
                   elif zz[0] ==2:
                      print("wrong")
                      cv2.putText(frame, "x", (200, 250), cv2.FONT_HERSHEY_DUPLEX,10, (0, 255, 255), 5, cv2.LINE_AA)
                      cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData) 
                   #sess.close()




    points = dict()  # change video name here !!!!!!!!!!!!!!!!!! until 11    12yet
    numFrame = 0
    nextFrame = 25
    currentDirection = 0
    predirection = 0
    handsHighest = 0
    serveFrames = 0
    number = 0
    normal = 0
    head=0
    neckX = 0
    neckY = 0
    shoulder = 0
    wait=0
    serveList=list()
        
    
    if not video.isOpened():
        print("Cannot open camera")
        exit()
    while(True):
           #print("wait",wait)
           ret, frame = video.read()
           
           if not ret:
              print("Can't receive frame (stream end?). Exiting ...")
              break
           if Right:
              frame = cv2.flip(frame,1) 
           # a = cv2.imshow(frame)
           #frame = cv2.transpose(frame)     # 90 degree(Winnie)
           #frame = cv2.flip(frame,1)        # left right
           #frame = cv2.flip(frame,-1)
           #h, w = frame.shape[:2]
           #print("h,w",h,w)
           #frame = cv2.resize(frame, (w//4, h//4), interpolation=cv2.INTER_AREA)
           datum.cvInputData = frame
           
           opWrapper.emplaceAndPop(op.VectorDatum([datum]))
           
           
           numFrame = numFrame + 1
           np.set_printoptions(precision=3)

           #temp = list(track.last_seen_detection.pose[:,0:2:1].reshape(-1))
           if datum.poseKeypoints is None or not ret:
              print("oops")
              currentPoints=list(np.zeros(50))
              points[numFrame]=currentPoints
              continue

           currentPoints=list(datum.poseKeypoints[0,:,0:2].reshape(-1))
           points[numFrame]=currentPoints.copy()
           if numFrame == 1 or head==0 or shoulder == 0 or normal == 0:
              head=datum.poseKeypoints[0,0,1]
              normal = points[numFrame][17]-points[numFrame][3]
              neckX=datum.poseKeypoints[0,1,0]
              neckY=datum.poseKeypoints[0,1,1]
              shoulder =  datum.poseKeypoints[0,2,1]
           else : 
              for i in range(int(len(currentPoints)/2)):
                 #print(points[numFrame][2*(i)],(points[numFrame][2*(i)]-neckX+500.0)/(normal*5))
                 points[numFrame][2*(i)]=(points[numFrame][2*(i)]-neckX+500.0)/(normal*5) if (currentPoints[(i)*2]) > 0 else 0.0
                 points[numFrame][2*(i)+1]=(points[numFrame][2*(i)+1]-neckY+500.0)/(normal*5) if (currentPoints[(i)*2+1]) > 0 else 0.0
              #print(numFrame,"datum.poseKeypoints[0,7,1]",datum.poseKeypoints[0,7,0],datum.poseKeypoints[0,7,1])
              if numFrame > nextFrame :
                if datum.poseKeypoints[0,4,1] < shoulder or datum.poseKeypoints[0,7,1] < shoulder :#hand
                  wait = 0
                  if datum.poseKeypoints[0,7,1] !=0 and (handsHighest == 0 or datum.poseKeypoints[0,7,1] < handsHighest) and datum.poseKeypoints[0,7,1] < head:# find tophand(left:small right:big)   #4: yellow(right), 7: green(left)
                     handsHighest = datum.poseKeypoints[0,7,1]
                     predirection = currentDirection
                     currentDirection =-1
                     #print("handsHighest",handsHighest)
                  elif numFrame > 10 :
                     predirection = currentDirection
                     currentDirection = 1#goright
                     leftangle = calculate_angle([datum.poseKeypoints[0,5,1],datum.poseKeypoints[0,5,0]], [datum.poseKeypoints[0,6,1],datum.poseKeypoints[0,6,0]], [datum.poseKeypoints[0,7,1],datum.poseKeypoints[0,7,0]])
                     if predirection == -1 and currentDirection == 1 and leftangle > 120 :#left to right (hand go down)
                        
                        nextFrame = numFrame +40
                        serveFrames = 0 
                        for i in range(numFrame-25,numFrame+1):
                           if i ==numFrame-25:
                               print("numFrame",numFrame-25,numFrame,numFrame+5)
                           servePoint=str(points[i]).replace(' ', '').replace('[','').replace(']','\n')
                           serveList.append(points[i])
                           #file.write(servePoint)
                           #print(i,":",servePoint)
                           #print(number,":",serveFrames)
                           serveFrames+=1
                  else :
                     predirection = currentdirection
                     currentdirection = 0
                else:
                  wait+=1
                  #print("wait",wait)
                  serveFrames =0
                  serveList.clear() 
           #print(str(numFrame) + "Body keypoints: \n" + str(currentpoints))
              elif serveFrames < 30 and serveFrames > 25:
                  servePoint=str(points[numFrame]).replace(' ', '').replace('[','').replace(']','\n')
                  #print(str(numFrame) + "Body keypoints: \n" + servePoint)
                  serveList.append(points[numFrame])               
                  #print(number,":",serveFrames)
                  #file.write(str(points[numFrame]).replace(' ', '').replace('[','').replace(']','\n'))
                  serveFrames+=1
              elif serveFrames == 30 :
                  serveFrames = 0 
                  handsHighest = 0
                  number+=1
                  file = open('success'+'_30.txt', 'a')
                  for servePoints in serveList : 
                      #print(c,"handspoints Body keypoints: \n",servepoints)
                      file.write(str(servePoints).replace(' ', '').replace('[','').replace(']','\n'))
                      #print(servepoints)
                      pose.append(servePoints)
                  serveList.clear()
                  file.close()
                  print(number)
                  print("-----------------------------------------------------------")
              else :
               
                  serveFrames = 0 
           
           if len(pose) == 30:
               classify(pose)
               pose.clear()
           if records : 
              out2.write(frame) 
           
           if Right == 1:
              cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", frame) 
           else :
              frame=cv2.flip(frame,1) 
              cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", frame)
           if cv2.waitKey(1) & 0xFF == ord('q'):break
           if number == 100 or wait==80:
               
               #print("correct:",final.count(1),"  wrong:",final.count(2),"accuracy:", (final.count(1)*100)//len(final),"%")   
               #messagebox.showinfo("Result", str("correct:",final.count(1),"  wrong:",final.count(2)))
               if len(final)==0:
                  messagebox.showerror("Warning", "correct:"+str(final.count(1))+"  wrong:"+str(final.count(2))+"\nWait for too long\n Please try again.")
               else : 
                  rate =(final.count(1)*100)/len(final)
               if rate >= 90:
                  messagebox.showinfo("Result", "correct:"+str(final.count(1))+"  wrong:"+str(final.count(2))+"\nYour score is S\n You are the best :)")
               elif rate >= 80:
                  messagebox.showinfo("Result", "correct:"+str(final.count(1))+"  wrong:"+str(final.count(2))+"\nYour score is A\n Excellent")
               elif rate >= 70:
                  messagebox.showinfo("Result", "correct:"+str(final.count(1))+"  wrong:"+str(final.count(2))+"\nYour score is B\n Nice")
               elif rate >= 60:
                  messagebox.showinfo("Result", "correct:"+str(final.count(1))+"  wrong:"+str(final.count(2))+"\nYour score is C\n You can do better.")
               else:
                  messagebox.showinfo("Result", "correct:"+str(final.count(1))+"  wrong:"+str(final.count(2))+"\nYour score is F\n Fail :(")
               #messagebox.showinfo("Time reminding", "Time's up")
               break
    #file.close()
    #print(cnt)
    video.release()
    out2.release()
    cv2.destroyAllWindows()
    print("end")
    '''
    fn = input('Enter file name: ')
    file = open(fn, 'w')
    start = time.time()
    print("start write ",num)
    for item in points :
       file.write(str(points[item]))
       print(points[item])
    end = time.time()
    file.close()
    '''


    #print("OpenPose demo successfully finished. Total time: " + str(end - start) + " seconds")
    if numFrame == 0:
        print("You are wrong")
  except Exception as e:
    print(e)
    sys.exit(-1)
if __name__ == '__main__': 
  dect_loop()
