import argparse
import os
import json
import time
from datetime import datetime

import numpy as np
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Create the model
model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

def main():
    model.load_weights('model.h5')

    # prevents openCL usage and unnecessary logging messages
    cv2.ocl.setUseOpenCL(False)

    # dictionary which assigns each label an emotion (alphabetical order)
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful",
                    3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

    # start the webcam feed
    cap = cv2.VideoCapture(0)
    begin = time.time()
    working = True
    fps = 1
    while True:

        try:
            with open('settings.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                working = data['work']
                fps = int(data['fps'])
        except FileNotFoundError:
            print("Configuracion no encontrada, ejecutando configuracion"
                  " por defecto")

        actual_time = time.time() - begin

        if working:
            if actual_time >= fps:
                # Find haar cascade to draw bounding box around face
                ret, frame = cap.read()
                if not ret:
                    break
                facecasc = cv2.CascadeClassifier('haarcascade_frontalface'
                                                 '_default.xml')
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = facecasc.detectMultiScale(gray, scaleFactor=1.3,
                                                  minNeighbors=5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y-50), (x+w, y+h+10),
                                  (255, 0, 0), 2)
                    roi_gray = gray[y:y + h, x:x + w]
                    roi_resized = cv2.resize(roi_gray, (48, 48))
                    cropped_img = np.expand_dims(np.expand_dims(roi_resized, -1), 0)
                    prediction = model.predict(cropped_img)
                    maxindex = int(np.argmax(prediction))
                    cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),
                                2, cv2.LINE_AA)

                cv2.imshow('Video', cv2.resize(frame, (1600, 960),
                                               interpolation=cv2.INTER_CUBIC))
                cv2.imwrite(f'{datetime.now()}.png', cv2.resize(frame, (1600, 960), interpolation=cv2.INTER_CUBIC))
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                begin = time.time()
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
