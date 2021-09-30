#lstm input  format
# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import time
import numpy as np
import re
import copy
def calculate_angle(a,b,c):#Clockwise
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])#radian
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
    return angle
try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Windows Import
        if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '/../../python/openpose/Release');
            os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
            import pyopenpose as op
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('../../python');
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_dir", default="../../examples/media/go.MP4", help="Process a directory of images. Read all standard formats (jpg, png, bmp, etc.).")
    parser.add_argument("--no_display", default=False, help="Enable to disable the visual display.")
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "../../models/"
    #params["hand"] = True       # for hand
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
    #imagePaths = cv2.VideoCapture(args[0].image_dir)    # start = time.time()
    #fn = input('Enter file name: ')
    numFrame = 0
    start = time.time()
    path = '../../examples/media/video/toss/test_18/toss_bad_43/toss_bad_43'
    file = open(path+'_18_4.txt', 'a')
    #except IOError:
        #file = open(fn, 'w')
        # Process and display images
        #for imagePath in imagePaths:
    datum = op.Datum()
    
    video = cv2.VideoCapture(path+'.mp4') 
    points = dict()
    point2array = []
    handmin = 0
    nexthandsframe = 14
    nextkneesframe = 14
    predirection = 0
    currentdirection = 0
    kneespredirection = 0
    kneescurrentdirection = 0
    handsframes = 0
    kneesframes = 0
    handscnt = 0
    kneescnt=0
    needtransfer=-1
    shoulder=0
    handlist=list()
    kneeslist=list()
    squences = list() #hands == 1 , knees =2
    while(video.isOpened()):
           ret, frame = video.read()
           # a = cv2.imshow(frame)
           #frame = cv2.transpose(frame)
           #frame = cv2.flip(frame,1)
           #frame = cv2.flip(frame,-1)
           h, w = frame.shape[:2]
           #print("h,w",h,w)
           frame = cv2.resize(frame, (w//4, h//4), interpolation=cv2.INTER_AREA)
           datum.cvInputData = frame
           
           opWrapper.emplaceAndPop(op.VectorDatum([datum]))
           
           
           numFrame = numFrame + 1
           np.set_printoptions(precision=3)
           #print("datum.poseKeypoints",datum.handKeypoints[0])
           #print("Left hand keypoints: \n" ,datum.handKeypoints[0])
           #print("Right hand keypoints: \n" ,datum.handKeypoints[1])
           if datum.poseKeypoints is None or not ret:
              print("oops")
              currentpoints=list(np.zeros(50))
              points[numFrame]=currentpoints
              continue
           #temp = list(track.last_seen_detection.pose[:,0:2:1].reshape(-1))
           currentpoints=list(datum.poseKeypoints[0,:,0:2].reshape(-1))
           points[numFrame]=currentpoints.copy()
           if numFrame == 0 or needtransfer ==-1 or shoulder == 0 or knees ==0 or waist ==0 :
              handsHighestL = 0
              handsHighestR = 0
              kneesLowestL = 0
              kneesLowestR = 0
              
              needtransfer = 1 if abs(datum.poseKeypoints[0,5,0]-datum.poseKeypoints[0,2,0]) > abs(datum.poseKeypoints[0,5,1]-datum.poseKeypoints[0,2,1]) else 0 
              neckX=datum.poseKeypoints[0,1,needtransfer]
              neckY=datum.poseKeypoints[0,1,(needtransfer+1)%2]
              shoulder =  datum.poseKeypoints[0,2,needtransfer]#rear
              knees = datum.poseKeypoints[0,13,needtransfer]
              if knees ==0:
                 knees = datum.poseKeypoints[0,10,needtransfer]
              waist = abs(datum.poseKeypoints[0,9,needtransfer]-datum.poseKeypoints[0,8,needtransfer])
              if waist ==0:
                 waist = abs(datum.poseKeypoints[0,8,needtransfer]-datum.poseKeypoints[0,12,needtransfer])
              print("shoulder",shoulder)
              print("knees",knees)
              print("needtransfer",needtransfer)
              normal =points[numFrame][16]-points[numFrame][2]
              if needtransfer :
                 normal = points[numFrame][17]-points[numFrame][3]
           else : 
             for i in range(int(len(currentpoints)/2)):
              if needtransfer :
                 points[numFrame][2*(i)]= (currentpoints[(i)*2+1]-neckX+500.0)/(normal*5)  if (currentpoints[(i)*2+1]) >0 else 0.0
                 points[numFrame][2*(i)+1]=(currentpoints[(i)*2]-neckY+500.0)/(normal*5)  if (currentpoints[(i)*2]) > 0 else 0.0
              else: 
                 points[numFrame][2*(i)]=(points[numFrame][2*(i)]-neckX+500.0)/(normal*5) if (currentpoints[(i)*2]) > 0 else 0.0
                 points[numFrame][2*(i)+1]=(points[numFrame][2*(i)+1]-neckY+500.0)/(normal*5) if (currentpoints[(i)*2+1]) > 0 else 0.0
             
             if numFrame > nexthandsframe :
               if datum.poseKeypoints[0,4,needtransfer] < shoulder or datum.poseKeypoints[0,7,needtransfer] < shoulder :#hand
                  if handsHighestL == 0 or datum.poseKeypoints[0,7,needtransfer] < handsHighestL and datum.poseKeypoints[0,7,needtransfer] !=0 :# find tophand(left:small right:big)
                     handsHighestL = datum.poseKeypoints[0,7,needtransfer]
                     predirection = currentdirection
                     currentdirection =-1
                  elif handsHighestR == 0 or datum.poseKeypoints[0,4,needtransfer] < handsHighestR  and datum.poseKeypoints[0,4,needtransfer] !=0: 
                     handsHighestR = datum.poseKeypoints[0,4,needtransfer]
                     predirection = currentdirection
                     currentdirection = -1# goleft
                  elif datum.poseKeypoints[0,7,needtransfer] ==0 and datum.poseKeypoints[0,4,needtransfer] ==0 :
                     points[numFrame]=points[numFrame-1]
                     continue
                  elif numFrame > 14 :
                     predirection = currentdirection
                     currentdirection = 1#goright
                     leftangle = calculate_angle([datum.poseKeypoints[0,5,needtransfer],datum.poseKeypoints[0,5,(needtransfer+1)%2]], [datum.poseKeypoints[0,6,needtransfer],datum.poseKeypoints[0,6,(needtransfer+1)%2]], [datum.poseKeypoints[0,7,needtransfer],datum.poseKeypoints[0,7,(needtransfer+1)%2]])
                     rightangle = calculate_angle([datum.poseKeypoints[0,2,needtransfer],datum.poseKeypoints[0,2,(needtransfer+1)%2]], [datum.poseKeypoints[0,3,needtransfer],datum.poseKeypoints[0,3,(needtransfer+1)%2]], [datum.poseKeypoints[0,4,needtransfer],datum.poseKeypoints[0,4,(needtransfer+1)%2]])
                     if (predirection == -1) and currentdirection == 1 and ( leftangle > 120 or rightangle > 120) :#left to right (hand go down)     
                        if datum.poseKeypoints[0,13,needtransfer]!=0:
                           knees = datum.poseKeypoints[0,13,needtransfer]
                        elif datum.poseKeypoints[0,13,needtransfer]!=0:
                           knees = datum.poseKeypoints[0,10,needtransfer]
                        print("hands high frame:",numFrame)
                        nexthandsframe = numFrame +20#bad_102 bad_101  30
                        handsframes = 0 
                        for i in range(numFrame-14,numFrame+1):
                           newpoint= copy.deepcopy(points[i])
                           newpoint[18::]=np.zeros(32)
                           currenthands=str(points[i]).replace(' ', '').replace('[','').replace(']','\n')
                           #currenthands=str(newpoint).replace(' ', '').replace('[','').replace(']','\n')
                           #print("currenthands",currenthands)
                           handlist.append(currenthands)
                           handsframes+=1
                  else :
                     predirection = currentdirection
                     currentdirection = 0
               else:
                 handsframes =0
                 handlist.clear() 
             elif handsframes < 18 and handsframes > 14:
               newpoint= copy.deepcopy(points[numFrame])
               newpoint[18::]=np.zeros(32)
               currenthands=str(points[numFrame]).replace(' ', '').replace('[','').replace(']','\n')
               #currenthands=str(newpoint).replace(' ', '').replace('[','').replace(']','\n')
               #print("currenthands",currenthands)
               handlist.append(currenthands)
               handsframes+=1
             elif handsframes == 18:
               handsframes = 0 
               handsHighestL = 0
               handsHighestR = 0

               currentdirection =0
               c=0
               handscnt+=1

               #label
               squences.append(1)

               #print("hands number",handscnt)
               for handspoints in handlist :
                   c+=1
                   print(c,"handspoints Body keypoints: \n",handspoints)
                   file.write(handspoints)
               handlist.clear()
               handsframes = 0 
               print(squences)
               print("-----------------------------------------------------------")
             else :
               handlist.clear()
               handsframes = 0 
               handsHighestL = 0
               handsHighestR = 0
             '''
             if numFrame > nextkneesframe :
                #print("abs",abs(kneesLowestL - knees) , abs(datum.poseKeypoints[0,9,needtransfer]-datum.poseKeypoints[0,8,needtransfer])/4 , abs(kneesLowestR - knees) , abs(datum.poseKeypoints[0,9,needtransfer]-datum.poseKeypoints[0,8,needtransfer])/4)
                #print("knees",datum.poseKeypoints[0,13,needtransfer],datum.poseKeypoints[0,10,needtransfer])
                if datum.poseKeypoints[0,13,needtransfer] >= knees or datum.poseKeypoints[0,10,needtransfer] >= knees :#hand
                  
                  if kneesLowestL == 0 or datum.poseKeypoints[0,13,needtransfer] > kneesLowestL and datum.poseKeypoints[0,13,needtransfer] !=0 :
                     kneesLowestL = datum.poseKeypoints[0,13,needtransfer]
                     kneespredirection = kneescurrentdirection
                     kneescurrentdirection =1

                  elif kneesLowestR == 0 or datum.poseKeypoints[0,10,needtransfer] > kneesLowestR  and datum.poseKeypoints[0,10,needtransfer] !=0: 
                     kneesLowestR = datum.poseKeypoints[0,10,needtransfer]
                     kneespredirection = kneescurrentdirection
                     kneescurrentdirection = 1# goleft

                  elif datum.poseKeypoints[0,13,needtransfer] ==0 and datum.poseKeypoints[0,10,needtransfer] ==0 :
                     points[numFrame]=points[numFrame-1]
                     continue

                  elif numFrame > 10 :
                     kneespredirection = kneescurrentdirection
                     kneescurrentdirection = -1#goright
                     if kneespredirection == 1 and kneescurrentdirection == -1 and (abs(kneesLowestL - knees) > (waist/4) or abs(kneesLowestR - knees) > (waist/4) ):
                        nextkneesframe = numFrame +18
                        kneesframes = 0      
                        print("knees low frame:",numFrame)

                        for i in range(numFrame-10,numFrame+1):
                           currentknees=str(points[i]).replace(' ', '').replace('[','').replace(']','\n')
                           kneeslist.append(currentknees)
                           kneesframes+=1
                  else :
                     kneespredirection = kneescurrentdirection
                     kneescurrentdirection = 0

             elif kneesframes < 18 and kneesframes > 10:
               currentknees=str(points[numFrame]).replace(' ', '').replace('[','').replace(']','\n')
               #print(str(i) + "Body keypoints: \n" + currenthands )
               kneeslist.append(currentknees)
               
               #file.write(str(points[numFrame]).replace(' ', '').replace('[','').replace(']','\n'))
               kneesframes+=1
             elif kneesframes == 18 :
               kneesframes = 0 
               kneesLowestL = 0
               kneesLowestR = 0
               kneescurrentdirection =0
               c=0
               kneescnt+=1

               #label
               squences.append(2)

               print("kneescnt",kneescnt)
               for kneespoints in kneeslist :
                   c+=1
                   #print(c,"kneespoints Body keypoints: \n",kneespoints)
                   file.write(kneespoints)
               kneeslist.clear()
               kneesframes = 0 
               print(squences)
               print("-----------------------------------------------------------")
           
             else :
               kneeslist.clear()
               kneesframes = 0 
               kneesLowestL = 0
               kneesLowestR = 0
             
             print("hands",handscnt,"knees",kneescnt , "total frame",(handscnt+kneescnt)*18 )
             '''
           print("hands",handscnt,"total frame",(handscnt)*18)
           cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)
           if cv2.waitKey(25) & 0xFF == ord('q'):break
    file.close()
    print("hands",handscnt,"knees",kneescnt )
    video.release()
    cv2.destroyAllWindows()

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

