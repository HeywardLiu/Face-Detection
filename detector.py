import cv2
import numpy as np
import datetime
import database
from database import COURSE_NAME, COURSE_DATE, print_roll_call_talbe


def detector(course_name, course_date):
    cam_id = 0
    face_casecade = cv2.CascadeClassifier('recognizer/haarcascade_frontalface_default.xml') #openCV裡，選取人臉範圍的套件
    webcam = cv2.VideoCapture(cam_id)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("recognizer\\trainingData.yml")
    pred_id=0
    font = cv2.FONT_HERSHEY_SIMPLEX #文字字型
    color = (255, 255, 255) #文字顏色
    stroke = 2 
    end=1
    
    while(end==1):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        ret, frame = webcam.read()
        cv2.putText(frame, "Press Q to terminate the program.", (50, 50) ,font, 1, color, stroke)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
        faces = face_casecade.detectMultiScale(gray, 1.3, 5)
        for(x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            pred_id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            student_id = database.format_id(pred_id)
            if(conf>110):
                student_id = "unknown"
            else:
                database.roll_call(course_name, course_date, student_id)

            cv2.putText(frame, str(student_id), (x,y+h), font, 1, color, stroke, )
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                end = end - 1
                break
                
        cv2.imshow('Face', frame)

    webcam.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    print_roll_call_talbe(COURSE_NAME)
    detector(COURSE_NAME, COURSE_DATE)
    print_roll_call_talbe(COURSE_NAME)