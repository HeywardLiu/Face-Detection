import os
import cv2
import numpy as np
from PIL import Image



def get_image_id(path):
    image_path = [os.path.join(path, f) for f in os.listdir(path)]
    faces=[]
    ids=[]

    for imagePath in image_path:
        face_img = Image.open(imagePath).convert('L')
        faceNp = np.array(face_img, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split('.')[1])
        print(ID)
        faces.append(faceNp)
        ids.append(ID)
        cv2.imshow("training", faceNp)
        cv2.waitKey(10)
    return ids, faces


def train_data_set():
    recognizer =  cv2.face.LBPHFaceRecognizer_create()
    path='dataSet'
    ids, faces = get_image_id(path)
    recognizer.train(faces, np.array(ids))
    recognizer.save('recognizer/trainingData.yml')
    cv2.destroyAllWindows()
