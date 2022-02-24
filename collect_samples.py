import cv2
import numpy as np
import database
from datetime import datetime


def register_new_id(course_name):
    try:
        user_first_name = str(input('your first name: '))
        user_last_name = str(input('your last name: '))
        user_id = str(input('your student ID: '))

    except:
        print() 
        exit("[Exception]: invalid input, register_new_id(), in file collect_samples.py, line 7")

    database.create_members_list(course_name)
    database.append_to_member_list(course_name, user_first_name, user_last_name, user_id)
    return user_id


def collect_samples(course_name):
    cam_id = 0
    sample_num = 0

    font = cv2.FONT_HERSHEY_SIMPLEX  # font style
    color = (255, 255, 255)  # font color 
    stroke = 2 
    end=1
    face_casecade = cv2.CascadeClassifier('recognizer/haarcascade_frontalface_default.xml')  
    webcam = cv2.VideoCapture(cam_id)
    user_id = register_new_id(course_name)
    database.print_roll_call_talbe(course_name)
    
    while(True):
        ret, frame = webcam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # gray scale to reduce computing workload.
        faces = face_casecade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        cv2.putText(frame, "Collecting samples... %d/100"%(sample_num), (50, 50) ,font, 1, color, stroke)
        for(x, y, w, h) in faces:
            sample_num += 1
            cv2.imwrite("dataSet/User."+str(user_id)+"."+str(sample_num)+".jpg", gray[y:y+h, x:x+w])  # collecting training samples from webcam
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), 2)                                   # save the picture to folder "dataSet"
            cv2.waitKey(100)
        cv2.imshow("Face", frame)    
        cv2.waitKey(1)

        if(sample_num>=100):  # Collect 100 samples
            cv2.waitKey(5)
            webcam.release()
            cv2.destroyAllWindows()
            break
        if cv2.waitKey(1) & 0xFF == ord('q'): # Press Q to terminate the process
            webcam.release()
            cv2.destroyAllWindows()
            break
