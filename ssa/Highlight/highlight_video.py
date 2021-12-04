
import cv2
import glob
def video(file_path):
 image_list = glob.glob('../../../../../../..'+file_path+'/img/*.jpg')
 image_list.sort()
 print(image_list)

 codec = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
 video = cv2.VideoWriter('../../../../../../..'+file_path+'/highlight.avi', codec, 25, (889, 689))

 for img_name in image_list:
    img = cv2.imread(img_name)
    img = cv2.resize(img, (889, 689))
    video.write(img)
 print("ya:)")
 video.release()
