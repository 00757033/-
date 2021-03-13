import cv2
import numpy
import torch
import time
import os
import subprocess 
a='cd ~/Downloads/openpose'
b='~/Downloads/openpose/build/examples/openpose/openpose.bin --video  ~/Downloads/openpose/examples/media/2.mp4 --write_keypoint  test/ --write_images output_images/ --write_images_format jpg --write_video test2/a.avi'
#n = os.system(a)
#m = os.system(b)
f = open('test/2_000000000000_pose.yml', 'r')
i=0
for line in f.readlines():
    line = line.strip()
    i+=1
    #print(line)
    if i==6:
        s1=(line.split("data: [")[0].split(","))
    elif i>6:
        s1.extend(line.split("]")[0].split(","))
#x=f.read()
d=f.read().splitlines()
f.close()
#s0=x.split("data[")
#s1=s0[1].split(",")
while("" in s1) : 
    s1.remove("") 
for j in range(len(s1)//8):
    print(s1[j:j+8])
print(len(s1)/8)