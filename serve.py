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
    path = '../../examples/media/video/serve/serve_bad_093004/serve_bad_093004'      #/serve_00857202
    file = open(path+'_30.txt', 'a')
    #except IOError:
        #file = open(fn, 'w')
        # Process and display images
        #for imagePath in imagePaths:
    datum = op.Datum()
    video = cv2.VideoCapture(path+'.mp4') 
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
    serveList=list()
    while(video.isOpened()):
           ret, frame = video.read()
           # a = cv2.imshow(frame)
           frame = cv2.transpose(frame)     # 90 degree(Winnie)
           #frame = cv2.flip(frame,1)        # left right
           #frame = cv2.flip(frame,-1)
           h, w = frame.shape[:2]
           #print("h,w",h,w)
           frame = cv2.resize(frame, (w//4, h//4), interpolation=cv2.INTER_AREA)
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
           if numFrame == 1 or head==0:
              head=datum.poseKeypoints[0,0,1]
              normal = points[numFrame][17]-points[numFrame][3]
              neckX=datum.poseKeypoints[0,1,0]
              neckY=datum.poseKeypoints[0,1,1]
           else : 
              for i in range(int(len(currentPoints)/2)):
                 #print(points[numFrame][2*(i)],(points[numFrame][2*(i)]-neckX+500.0)/(normal*5))
                 points[numFrame][2*(i)]=(points[numFrame][2*(i)]-neckX+500.0)/(normal*5) if (currentPoints[(i)*2]) > 0 else 0.0
                 points[numFrame][2*(i)+1]=(points[numFrame][2*(i)+1]-neckY+500.0)/(normal*5) if (currentPoints[(i)*2+1]) > 0 else 0.0
              #print(numFrame,"datum.poseKeypoints[0,7,1]",datum.poseKeypoints[0,7,0],datum.poseKeypoints[0,7,1])
              if numFrame > nextFrame :
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
                           serveList.append(servePoint)
                           #file.write(servePoint)
                           #print(i,":",servePoint)
                           #print(number,":",serveFrames)
                           serveFrames+=1
                  else :
                     predirection = currentdirection
                     currentdirection = 0
           #print(str(numFrame) + "Body keypoints: \n" + str(currentpoints))
                     '''
           if numFrame == 0 or normalizeX ==0 or normalizeY ==0 or boundaryX == 0:
              cmpmin = 0
              needtransfer = 1 if abs(datum.poseKeypoints[0,5,0]-datum.poseKeypoints[0,2,0]) > abs(datum.poseKeypoints[0,5,1]-datum.poseKeypoints[0,2,1]) else 0
              normalizeX=datum.poseKeypoints[0,1,needtransfer]
              normalizeY=datum.poseKeypoints[0,1,(needtransfer+1)%2]
              handmin = datum.poseKeypoints[0,2,needtransfer]#rear
              print("needtransfer",needtransfer)
              normal =points[numFrame][16]-points[numFrame][2]
              if needtransfer :
                 normal = points[numFrame][17]-points[numFrame][3]
              if datum.poseKeypoints[0,2,needtransfer]!=0 and datum.poseKeypoints[0,17,needtransfer]!=0:
                 boundaryX = datum.poseKeypoints[0,17,needtransfer]#datum.poseKeypoints[0,2,needtransfer]*1/4+datum.poseKeypoints[0,17,needtransfer]*3/4
                 print("boundaryX",datum.poseKeypoints[0,17,needtransfer],datum.poseKeypoints[0,17,(needtransfer+1)%2])
           else :
             if datum.poseKeypoints[0,2,needtransfer]!=0 and datum.poseKeypoints[0,17,needtransfer]!=0:
                 boundaryX = datum.poseKeypoints[0,17,needtransfer]#datum.poseKeypoints[0,2,needtransfer]*1/4+datum.poseKeypoints[0,17,needtransfer]*3/4
             for i in range(int(len(currentpoints)/2)):
              if needtransfer :
                 points[numFrame][2*(i)]= (currentpoints[(i)*2+1]-normalizeX+500.0)/(normal*5)  if (currentpoints[(i)*2+1]) >0 else 0.0
                 points[numFrame][2*(i)+1]=(currentpoints[(i)*2]-normalizeY+500.0)/(normal*5)  if (currentpoints[(i)*2]) > 0 else 0.0
              else: 
                 points[numFrame][2*(i)]=(points[numFrame][2*(i)]-normalizeX+500.0)/(normal*5) if (currentpoints[(i)*2]) > 0 else 0.0
                 points[numFrame][2*(i)+1]=(points[numFrame][2*(i)+1]-normalizeY+500.0)/(normal*5) if (currentpoints[(i)*2+1]) > 0 else 0.0
           
             #print("show",points[numFrame])
             #print(normal,"show",points[numFrame][5],points[numFrame][11])
             # 7isleft 4isright
             if numFrame > nextframe :  
               if datum.poseKeypoints[0,4,needtransfer] < boundaryX and datum.poseKeypoints[0,4,needtransfer] !=0:#rear
                  print(datum.poseKeypoints[0,4,needtransfer],boundaryX,datum.poseKeypoints[0,17,needtransfer],datum.poseKeypoints[0,17,(needtransfer+1)%2])
                  if cmpmin == 0 or datum.poseKeypoints[0,4,needtransfer] < cmpmin  and datum.poseKeypoints[0,4,needtransfer] !=0: 
                     cmpmin = datum.poseKeypoints[0,4,needtransfer]
                  elif numFrame > 7 :
                     cmpmin = 0 
                     nextframe = numFrame +25
                     serveframes = 0 
                     for i in range(numFrame-7,numFrame+1):
                        if i ==numFrame-7:
                           print("numFrame",numFrame)
                        currentserve=str(points[i]).replace(' ', '').replace('[','').replace(']','\n')
                        #print(str(i) + "Body keypoints: \n" + currentserve)
                        servelist.append(currentserve)
                        #file.write(str(points[i]).replace(' ', '').replace('[','').replace(']','\n'))
                        serveframes+=1
                  else :
                     continue
                     
               else:
                  continue
                  
               #print(numFrame ," : ","predirection",predirection,"currentdirection",currentdirection)
                     '''
              elif serveFrames < 30 and serveFrames > 25:
                  servePoint=str(points[numFrame]).replace(' ', '').replace('[','').replace(']','\n')
                  #print(str(numFrame) + "Body keypoints: \n" + servePoint)
                  serveList.append(servePoint)               
                  #print(number,":",serveFrames)
                  #file.write(str(points[numFrame]).replace(' ', '').replace('[','').replace(']','\n'))
                  serveFrames+=1
              elif serveFrames == 30 :
                  serveFrames = 0 
                  handsHighest = 0
                  number+=1
                  for servePoints in serveList : 
                      #print(c,"handspoints Body keypoints: \n",servepoints)
                      file.write(servePoints)
                      #print(servepoints)
                  serveList.clear()
                  print(number)
                  print("-----------------------------------------------------------")
              else :
               
                  serveFrames = 0 
           
           cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)
           if cv2.waitKey(1) & 0xFF == ord('q'):break
    file.close()
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

