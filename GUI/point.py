#lstm input  format
# From Python
# It requires OpenCV installed for Python
#Separate
import sys
import cv2
import os
from sys import platform
import argparse
import time
import numpy as np
import re
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
    numFrame = 0
    start = time.time()
    path = '../../../examples/media/video/highlight/spike_6/spike_6'
    pathimage = '../../../examples/media/video/highlight/spike_6/'
    file = open(path+'_1.txt', 'a')
    #except IOError:
        #file = open(fn, 'w')
        # Process and display images
        #for imagePath in imagePaths:
    datum = op.Datum()
    video = cv2.VideoCapture(path+'.mp4') 
    points = dict()  # change video name here !!!!!!!!!!!!!!!!!! until 11    12yet
    image =dict()
    point2array = []
    handmin = 0
    nextframe = 8
    nextframe_serve = 8
    nextFrameImg=-1
    currentdirection = 0
    serveframes = 0
    cnt = 0
    needtransfer=-1
    normalizeX=0
    normalizeY=0
    normal = 0
    countto3=1
    countto3_lock=0
    countto3_serve=1
    countto3_lock_serve=0
    countto3_save=1
    countto3_lock_save=0
    g=0
    highlist=list()
    servelist=list()
    savelist=list()
    
    while(video.isOpened()):
           ret, frame = video.read()


           h, w = frame.shape[:2]
           #print("h,w",h,w)
           frame = cv2.resize(frame, (w//4, h//4), interpolation=cv2.INTER_AREA)
           datum.cvInputData = frame           
           opWrapper.emplaceAndPop(op.VectorDatum([datum]))
           currentimage=list(frame)
           image[numFrame]=frame          
           numFrame = numFrame + 1
           np.set_printoptions(precision=3)
           print(":)", numFrame,nextFrameImg)
           if  numFrame<=nextFrameImg:
              if numFrame not in highlist:
                 print(":(")
                 cv2.imwrite(pathimage+"frame %d.jpg" % numFrame, frame)
                 #print(index)
                 highlist.append(numFrame)
                          
                 highlist=sorted(highlist)
          

           
           def findmin(Min):
               cmpmin=1000
              
               for i in Min:
                #print(type(i),i)

               	if i!=0 and i<cmpmin:
                   cmpmin=i
               return cmpmin
           def checkexist(point):
               count=0
              
               for i in point:
                

               	if i==0 :
                   count=count+1

               return count
           
           
           #temp = list(track.last_seen_detection.pose[:,0:2:1].reshape(-1))
           if datum.poseKeypoints is None or not ret:
              print("oops")
              currentpoints=list(np.zeros(50))
              points[numFrame]=currentpoints
              continue
           

           for i in range(0,len(datum.poseKeypoints)):

                currentpoints=list(datum.poseKeypoints[i,:,0:2].reshape(-1))                   

                countto3_lock=0
                countto3_lock_serve=0
                countto3_lock_save=0
                if len(datum.poseKeypoints)>9 and len(datum.poseKeypoints)<=13:
                  allplace=list()
                  allplace=[]
                  #print(numFrame,"'s people",len(datum.poseKeypoints))
                  currentminx=list(datum.poseKeypoints[i,:,0].reshape(-1))
                  currentmaxx=list(datum.poseKeypoints[i,:,0].reshape(-1))
                  currentminy=list(datum.poseKeypoints[i,:,1].reshape(-1))
                  currentmaxy=list(datum.poseKeypoints[i,:,1].reshape(-1))
                  #print(numFrame,"'s minx",i,":"+str(currentminx))
                  #print(numFrame,"'s miny",i,":"+str(currentminy))
                  #print(numFrame,"'s minx",i,":"+str(currentmaxx))
                  
                  #print(numFrame,"'s minx",i,":"+str(findmin(currentminx)))
                  #print(numFrame,"'s maxx",i,":"+str(max(currentmaxx)))
                  #print(numFrame,"'s miny",i,":"+str(findmin(currentminy)))
                  #print(numFrame,"'s ",i,":"+str(max(currentmaxy)))
                  heightpoint=max(currentmaxy)-min(currentminy)
                  widthpoint=max(currentmaxx)-min(currentminx)
                  #print("++   ",str(findmin(currentminy))==datum.poseKeypoints[i,4,1])
                    



                  #####high
                  if findmin(currentminy)==datum.poseKeypoints[i,4,1] or findmin(currentminy)==datum.poseKeypoints[i,7,1] :#hand is the highest


                    if countto3==3 and numFrame<=nextframe and countto3_lock==0 and heightpoint/widthpoint>1.5 and checkexist(datum.poseKeypoints[i,:,0])<4 and datum.poseKeypoints[i,0,0]!=0:
                      print ("high: ",numFrame,datum.poseKeypoints[i,0,0]," ",datum.poseKeypoints[i,0,1],heightpoint/widthpoint,checkexist(datum.poseKeypoints[i,:,0]))
                      countto3=1
                      countto3_lock=1

                      for index in range(numFrame-10,numFrame-1,1):
                        nextImg=1
                        nextFrameImg=numFrame+10
                        if index not in highlist:
                          cv2.imwrite(pathimage+"frame %d.jpg" % index, image[index])
                          #print(index)
                          highlist.append(index)
                          
                      highlist=sorted(highlist)
                
                      print("##################",sorted(highlist))
                      
                    elif countto3<3 and countto3>1 and numFrame<=nextframe and countto3_lock==0 :
                      print(numFrame," ",i,"countto3==2")
                      countto3=countto3+1
                      countto3_lock=1
                    elif countto3==1 and countto3_lock==0:
                      print(numFrame," ",i,"countto3==1")
                      countto3=countto3+1
                      nextframe=numFrame+3
                      countto3_lock=1
                    elif numFrame>nextframe:
                      countto3=1
                      countto3_lock=0
                
                  ##########serve
                  if findmin(currentminy)==datum.poseKeypoints[i,4,1] or findmin(currentminy)==datum.poseKeypoints[i,7,1] :
                    #print("here",numFrame," ",i)

                    for ii in range(0,len(datum.poseKeypoints)):
                        if datum.poseKeypoints[ii,0,0] !=0:
                           allplace.append(datum.poseKeypoints[ii,0,0]) 

                    #print(datum.poseKeypoints[i,0,0],allplace)
                    if (datum.poseKeypoints[i,0,0] == min(allplace) or datum.poseKeypoints[i,0,0] == max(allplace)) and datum.poseKeypoints[i,0,0]!=0 and checkexist(datum.poseKeypoints[i,:,0])<4 :
                           print("serve          ",datum.poseKeypoints[i,0,0] ,countto3_serve, countto3_lock_serve,numFrame,nextframe_serve, checkexist(datum.poseKeypoints[i,:,0]))
                           g=0
                    else:
                           g=1
                     
                    if countto3_serve==2 and countto3_lock_serve==0 and g==0 and numFrame<=nextframe_serve:
                    
                      
                      countto3_serve=1
                      for index in range(numFrame-10,numFrame+10,1):
                        if index not in servelist:
                          #print(index)
                          servelist.append(index) 
                      servelist=sorted(servelist)
                      print("#########servelist#########",sorted(servelist))
                    elif countto3_serve==1 and countto3_lock_serve==0 and g==0:
                      print(numFrame," ",i,"serve==1")
                      countto3_serve=countto3_serve+1
                      nextframe_serve=numFrame+3#range big
                      countto3_lock_serve=1

                    elif numFrame>nextframe_serve :
                      countto3_serve=1
                      countto3_lock_serve=0

               

                points[numFrame]=currentpoints.copy()
           
           #print(str(numFrame) + "Body keypoints: \n" + str(currentpoints))
          
           
             #print("show",points[numFrame])
             #print(normal,"show",points[numFrame][5],points[numFrame][11])
             # 7isleft 4isright
            
           currentserve=str(points[numFrame]).replace(' ', '').replace('[','').replace(']','\n')     
           #print('numFrame',numFrame," ",currentserve)
           

           
           cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)
           if cv2.waitKey(1) & 0xFF == ord('q'):break
    file.close()
    print(cnt)

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
    print(highlist)
    print(servelist)
    if numFrame == 0:
        print("You are wrong")
except Exception as e:
    print(e)
    sys.exit(-1)

