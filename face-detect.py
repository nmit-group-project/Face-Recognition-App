# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 12:33:38 2019

@author: Prajna Shetty
"""
import cv2
import os

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
if __name__ == "__main__":

    vid = cv2.VideoCapture(0)
    folder="Data/" + input("name : ")
    if not os.path.exists(folder):
            os.makedirs(folder)
            count =1
            success = 1

            while success:
                success, img = vid.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x,y,w,h) in faces:
                    name=folder+"/frame%d.jpg" % count
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,0),2)
                    roi_color = img[y:y+h, x:x+w]
                    print ('Creating...' + name)
                    cv2.imwrite(name,roi_color)
                    count += 1
                    
                cv2.imshow('img',img)
                if name==(folder+"/frame400.jpg"):
                    break;
                k = cv2.waitKey(30) & 0xff
                if k == 27:
                    break

            vid.release()
            cv2.destroyAllWindows()

    else:
        print("student already present")