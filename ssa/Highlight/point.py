# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 16:57:22 2021

@author: 00857202
"""

#lstm input  format
# From Python
# It requires OpenCV installed for Python
#Separate
import sys
import tkinter as tk, threading
import cv2
import os
from sys import platform
import argparse
import time
import numpy as np
import re
import shutil
import Highlight.highlight_video
import glob
import subprocess
import pathlib


def highlight(file_path):
   #print("file_path",file_path)
   #pathimage ='../../../../../../../../..'+file_path+'/img/'
   #print("now_path",os.path.dirname(os.path.realpath(__file__)))
   #print(pathimage)
   try:
    # Import Openpose (Windows/Ubuntu/OSX)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:
           #print("hi")
        # Windows Import
           if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '/../../../../python/openpose/Release');
            os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../../x64/Release;' +  dir_path + '/../../bin;'
            import pyopenpose as op
           else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('../../../..python');
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            import pyopenpose as op
        except ImportError as e:
           print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
           raise e

    # Flags
        parser = argparse.ArgumentParser()
        parser.add_argument("--image_dir", default="../../../../examples/media/go.MP4", help="Process a directory of images. Read all standard formats (jpg, png, bmp, etc.).")
        parser.add_argument("--no_display", default=False, help="Enable to disable the visual display.")
        args = parser.parse_known_args()

        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        params = dict()
        params["model_folder"] = "../../../models/"
        #print("model_folder",params["model_folder"])
        
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
        img1 = cv2.imread('pic/ssa.png')
        width = int(img1.shape[1] * 70 / 300) 
        height = int(img1.shape[0] * 70 / 300) 
        rows, cols= img1.shape[:2]
        dim = (width, height) # 圖片形狀 


        os.makedirs('../../../../../../..'+file_path+'/img/',exist_ok=True)
        
        pathimage ='../../../../../../..'+file_path+'/img/'
        #pathimage_save ='../../../../../../..'+file_path+'/img2/'
        #shutil.rmtree('../../../../../../..'+file_path+'/img2/', ignore_errors=True)
        shutil.rmtree('../../../../../../..'+file_path+'/img/', ignore_errors=False)
        os.makedirs('../../../../../../..'+file_path+'/img/',exist_ok=True)
        #os.makedirs('../../../../../../..'+file_path+'/img2/',exist_ok=True)

        path = '../../../../../../..'+file_path    
        #print(path)
        datum = op.Datum()
        video = cv2.VideoCapture(path+'.mp4') 
        #print(video)
        points = dict()  # change video name here !!!!!!!!!!!!!!!!!! until 11    12yet
        image =dict()
        point2array = []
        handmin = 0
        nextframe = 8
        nextframe_save = 8
        nextFrameImg=-1
        nextFrameImg_save=-1
        currentdirection = 0
        saveframes = 0
        cnt = 0
        needtransfer=-1
        normalizeX=0
        normalizeY=0
        normal = 0
        countto3=1
        countto3_lock=0
        countto3_save=1
        countto3_lock_save=0
        countto3_save=1
        countto3_lock_save=0
        plustwovideo=0
        g=0
        x=0
        y=0
        segmentation=0
        newx = x
        high_point_x=0
        high_point_y=0
        biggerthan30=0
        highlist=list()
        spikelist=list()
        savelist=list()
       
        while(video.isOpened()):
               ret, frame = video.read()
               #print("123")
    
               h, w = frame.shape[:2]
               #print("h,w",h,w)
               frame = cv2.resize(frame, (w//2, h//2), interpolation=cv2.INTER_AREA)
               datum.cvInputData = frame           
               opWrapper.emplaceAndPop(op.VectorDatum([datum]))
               frame_width=cv2.CAP_PROP_FRAME_WIDTH
               frame_height=cv2.CAP_PROP_FRAME_HEIGHT
               currentimage=list(frame)
               image[numFrame]=frame.copy()          
               numFrame = numFrame + 1
               np.set_printoptions(precision=3)
               #print(":)", numFrame)
    
              
               def checkonlyonehand(x,y,z):
                   count=0
                   if x<z:
                      count=count+1
                   if y<z:
                      count=count+1
                   return count
                      
               
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
                    
                     if i==0:
                        count=count+1
    
                   return count
               def checkexist_all(point,n):
    
                    count_people=0
                  
                    for index in range(0,len(point)):
                     count=0
                     for i in point[index,:,0]:
                        #print("frame",n,count_people,i)
                   	    if i==0 :
                               #print("count",count+1)
                               count=count+1
    
                     if count<4:
                        count_people=count_people+1
                        #print("564465",n,count,count_people)
    
                    return count_people
               
               
               #temp = list(track.last_seen_detection.pose[:,0:2:1].reshape(-1))
               if datum.poseKeypoints is None or not ret:
                  #print("oops")
                  currentpoints=list(np.zeros(50))
                  points[numFrame]=currentpoints
                  continue
               
    
               for i in range(0,len(datum.poseKeypoints)):
                   
                    currentpoints=list(datum.poseKeypoints[i,:,0:2].reshape(-1))                   
    
                    countto3_lock=0
                    countto3_lock_serve=0
                    countto3_lock_save=0             
                    if checkexist_all(datum.poseKeypoints,numFrame)>=9 and checkexist_all(datum.poseKeypoints,numFrame)<=13:
                      allplace=list()
                      allplace=[]
                      #print(numFrame,"'s people",checkexist_all(datum.poseKeypoints,numFrame))
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
                      heightpoint=max(currentmaxy)-findmin(currentminy)
                      widthpoint=max(currentmaxx)-findmin(currentminx)
                      #print("++   ",heightpoint/widthpoint)
                        
    
                         #print("590",countto3,findmin(currentminy),datum.poseKeypoints[i,4,1],datum.poseKeypoints[i,7,1],numFrame,nextFrameImg , countto3_lock==0 , heightpoint/widthpoint, checkexist(datum.poseKeypoints[i,:,0])<4 , datum.poseKeypoints[i,0,0]!=0)
    
                      #####high
                      if (findmin(currentminy)==datum.poseKeypoints[i,4,1] or findmin(currentminy)==datum.poseKeypoints[i,7,1]) and (heightpoint/widthpoint)>2.5 and checkexist(datum.poseKeypoints[i,:,0])<4:#hand is the highest
    
    
                        if countto3==8 and numFrame<=nextframetemp and countto3_lock==0  :
                            
                          #print ("high: ",numFrame,datum.poseKeypoints[i,0,0]," ",datum.poseKeypoints[i,0,1],heightpoint/widthpoint,checkexist(datum.poseKeypoints[i,:,0]))
                          countto3=1
                          countto3_lock=1
                          
                          for index in range(numFrame-20,numFrame-1,1):
                            nextImg=1
                            nextFrameImg=numFrame+60 
                            
                            segmentation=int(index)-1
                            
                            if index not in highlist :
    
                              
                              #print("index-----------------------",numFrame,nextFrameImg,index,heightpoint/widthpoint) 

                              cv2.imwrite(pathimage+"frame %d.jpg" % index, image[index])
                              #print(index)
                              highlist.append(index)
                              #print(segmentation,highlist,savelist)
                              high_point_x_last30=datum.poseKeypoints[i,0,0]
                              high_point_y_last30=datum.poseKeypoints[i,0,1]
                              if  segmentation not in highlist+savelist:
                                for ten in range(0,10,1):
                                   #print(index)
                                   cv2.imwrite(pathimage+"frame "+str(segmentation)+"_"+str(ten)+".jpg", img1) 
                              
                          highlist=sorted(highlist)
                    
                          #print("##################",sorted(highlist))
                          
                        elif countto3<8 and countto3>1 and numFrame<=nextframetemp and countto3_lock==0 :
                          #print(numFrame," ",i,"countto3==2")
                          countto3=countto3+1
                          countto3_lock=1
                        elif countto3==1 and countto3_lock==0:
                          #print(numFrame," ",i,"countto3==1")
                          countto3=countto3+1
                          nextframetemp=numFrame+10
                          countto3_lock=1
                        elif numFrame>nextframetemp:
                          #print(numFrame,"next",nextframetemp)
                          countto3=1
                          countto3_lock=0


                      #####save
                      
                      if (findmin(currentminy)==datum.poseKeypoints[i,4,1] or findmin(currentminy)==datum.poseKeypoints[i,7,1]) and (heightpoint/widthpoint)<0.65 and checkexist(datum.poseKeypoints[i,:,0])<4:#hand is the highest
                        #print(numFrame)
    
                        if countto3_save==2 and numFrame<=nextframetemp_save and countto3_lock_save==0  :
                          #print ("high: ",numFrame,datum.poseKeypoints[i,0,0]," ",datum.poseKeypoints[i,0,1],heightpoint/widthpoint,checkexist(datum.poseKeypoints[i,:,0]))
                          countto3_save=1
                          countto3_lock_save=1
                          x=datum.poseKeypoints[i,0,0]
                          y=datum.poseKeypoints[i,0,1]
             
                          for index in range(numFrame-150,numFrame-1,1):
                            nextImg_save=1
                            nextFrameImg_save=numFrame+60 
                            
                            segmentation_save=int(index)-1
                            
                            if index not in savelist :
    
                              if index>numFrame-100:
                              #print("index-----------------------",numFrame,nextFrameImg_save,index,heightpoint/widthpoint) 
                                 cv2.putText(image[index], "Nice", (250, 200), cv2.FONT_HERSHEY_DUPLEX,5, (0, 255, 255), 2, cv2.LINE_AA)
                                 cv2.putText(image[index], "o", (x, y), cv2.FONT_HERSHEY_DUPLEX,8, (0, 255, 255), 2, cv2.LINE_AA)
                              cv2.imwrite(pathimage+"frame %d.jpg" % index, image[index])
                              #print(index)
                              savelist.append(index)

                              if  segmentation_save not in highlist+savelist:
                                for ten in range(0,10,1):
                                   #print(index)
                                   cv2.imwrite(pathimage+"frame "+str(segmentation_save)+"_"+str(ten)+".jpg", img1) 
                              
                          savelist=sorted(savelist)
                    
                          #print("##################",sorted(savelist))
                          
                        elif countto3_save<2 and countto3_save>1 and numFrame<=nextframetemp_save and countto3_lock_save==0 :
                          #print(numFrame," ",i,"countto3==2")
                          countto3_save=countto3_save+1
                          countto3_lock_save=1
                        elif countto3_save==1 and countto3_lock_save==0:
                          #print(numFrame," ",i,"countto3==1")
                          countto3_save=countto3_save+1
                          nextframetemp_save=numFrame+10
                          countto3_lock_save=1
                        elif numFrame>nextframetemp_save:
                          #print(numFrame,"next",nextframetemp)
                          countto3_save=1
                          countto3_lock_save=0
                      
    
                       
    
    
                    if  numFrame<=nextFrameImg:
                       
                        if numFrame not in highlist+savelist:
                          #print(":(")
                          
                          cv2.imwrite(pathimage+"frame %d.jpg" % numFrame, frame)
    
                          #print(index)
                          highlist.append(numFrame)
                              
                          highlist=sorted(highlist) 
    
    
                    if  numFrame<=nextFrameImg_save: 
                        if numFrame not in highlist+savelist:
                          #print(":(")
                          
                          cv2.imwrite(pathimage+"frame %d.jpg" % numFrame, frame)
    
                          #print(index)
                          savelist.append(numFrame)
                              
                          savelist=sorted(savelist) 

                    
    
                    points[numFrame]=currentpoints.copy()
               
               if numFrame % 50 >=0 and numFrame % 50 <5: 
                  cv2.putText(frame,"A", (40,140),cv2.FONT_HERSHEY_DUPLEX,3, (255,255,255), 1, cv2.LINE_AA)#Draw the text 
               if numFrame % 50 >=5 and numFrame % 50 <10: 
                  cv2.putText(frame,"An", (40,140),cv2.FONT_HERSHEY_DUPLEX,3, (255,255,255), 1, cv2.LINE_AA)#Draw the text 
               if numFrame % 50 >=10 and numFrame % 50 <15: 
                  cv2.putText(frame,"Ana", (40,140),cv2.FONT_HERSHEY_DUPLEX,3, (255,255,255), 1, cv2.LINE_AA)#Draw the text 
               if numFrame % 50 >=15 and numFrame % 50 <20: 
                  cv2.putText(frame,"Anal", (40,140),cv2.FONT_HERSHEY_DUPLEX,3, (255,255,255), 1, cv2.LINE_AA)#Draw the text 
               if numFrame % 50 >=20 and numFrame % 50 <25: 
                  cv2.putText(frame,"Analy", (40,140),cv2.FONT_HERSHEY_DUPLEX,3, (255,255,255), 1, cv2.LINE_AA)#Draw the text 
               if numFrame % 50 >=25 and numFrame % 50 <30: 
                  cv2.putText(frame,"Analyz", (40,140),cv2.FONT_HERSHEY_DUPLEX,3, (255,255,255), 1, cv2.LINE_AA)#Draw the text 
               if numFrame % 50 >=30 and numFrame % 50 <35: 
                  cv2.putText(frame,"Analyze", (40,140),cv2.FONT_HERSHEY_DUPLEX,3, (255,255,255), 1, cv2.LINE_AA)#Draw the text 
               if numFrame % 50 >=35 and numFrame % 50 <40: 
                  cv2.putText(frame,"Analyze.", (40,140),cv2.FONT_HERSHEY_DUPLEX,3, (255,255,255), 1, cv2.LINE_AA)#Draw the text 
               if numFrame % 50 >=40 and numFrame % 50 <45:                  
                  cv2.putText(frame,"Analyze..", (40,140),cv2.FONT_HERSHEY_DUPLEX,3, (255,255,255), 1, cv2.LINE_AA)#Draw the text 
               if numFrame % 50 >=45 and numFrame % 50 <50:                  
                  cv2.putText(frame,"Analyze...", (40,140),cv2.FONT_HERSHEY_DUPLEX,3, (255,255,255), 1, cv2.LINE_AA)#Draw the text
               cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", frame)
     
               if cv2.waitKey(1) & 0xFF == ord('q'):
                  #print("i am here")
                  break
        #print("123")
        #video.release()
        #cv2.destroyAllWindows()
    
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

        image_list = glob.glob('../../../../../../..'+file_path+'/img/*.jpg')
        image_list.sort()
        #print(image_list)

        codec = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
        video = cv2.VideoWriter('../../../../../../..'+file_path+'/highlight.avi', codec, 25, (889, 689))

        #image_list_save = glob.glob('../../../../../../..'+file_path+'/img2/*.jpg')
        #image_list_save.sort()
        #print(image_list)

        #codec_save = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
        #video_save = cv2.VideoWriter('../../../../../../..'+file_path+'/highlight2.avi', codec_save, 25, (889, 689))

        for img_name in image_list:
            img = cv2.imread(img_name)
            img = cv2.resize(img, (889, 689))
            video.write(img)
        #for img_name in image_list_save:
            #img = cv2.imread(img_name)
            #img = cv2.resize(img, (889, 689))
            #video_save.write(img)
        print("ya:):)")
        shutil.rmtree('../../../../../../..'+file_path+'/img', ignore_errors=True)
        #shutil.rmtree('../../../../../../..'+file_path+'/img2', ignore_errors=True)
        #subprocess.Popen('../../../../../../..'+file_path+'/highlight.avi')
        video.release()
        cv2.destroyAllWindows()
        #sys.exit(-1)


if __name__ == '__main__': 
    highlight()

