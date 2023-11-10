import argparse
import os
import json
import time
from datetime import datetime

import numpy as np
import cv2
import tensorflow.lite as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def main():

    result_path = 'results'
    if not os.path.exists(result_path):
        os.mkdir(result_path)

    interpreter = tf.Interpreter(model_path="D:\Taller_Emb\proyecto2_TSE\emociones\model.tflite")
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # prevents openCL usage and unnecessary logging messages
    cv2.ocl.setUseOpenCL(False)

    # dictionary which assigns each label an emotion (alphabetical order)
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful",
                    3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

    data = {'work': True, 'spf': 1}

    try:
        with open('settings.json', 'r', encoding='utf-8') as f:
            data['spf'] = json.load(f)['spf']
    except FileNotFoundError:
        print("Configuracion no encontrada, ejecutando configuracion"
              " por defecto")

    with open('settings.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)

    # start the webcam feed
    cap = cv2.VideoCapture(0)
    begin = time.time()

    while True:

        try:
            with open('settings.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                working = data['work']
                spf = int(data['spf'])
        except FileNotFoundError:
            print("Configuracion no encontrada, ejecutando configuracion"
                  " por defecto")

        facecasc = cv2.CascadeClassifier('haarcascade_frontalface'
                                         '_default.xml')
        actual_time = time.time() - begin

        if working:

            # Find haar cascade to draw bounding box around face
            ret, frame = cap.read()
            if not ret:
                break

            if actual_time >= spf:

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = facecasc.detectMultiScale(gray, scaleFactor=1.3,
                                                  minNeighbors=5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y-50), (x+w, y+h+10),
                                  (255, 0, 0), 2)
                    roi_gray = gray[y:y + h, x:x + w]
                    roi_resized = cv2.resize(roi_gray, (48, 48))
                    cropped_img = np.expand_dims(np.expand_dims(roi_resized, -1), 0)
                    interpreter.set_tensor(input_details[0]['index'], cropped_img.astype(np.float32))
                    interpreter.invoke()
                    prediction = interpreter.get_tensor(output_details[0]['index'])
                    maxindex = int(np.argmax(prediction))
                    cv2.putText(frame, emotion_dict[maxindex], (x+20, y-60),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),
                                2, cv2.LINE_AA)

                    result_name = datetime.now()
                    cv2.imwrite(f'results/{result_name}.png',
                                cv2.resize(frame, (500, 300), interpolation=cv2.INTER_CUBIC))

                    with open('results/resultados.txt', 'a', encoding='utf-8') as f:
                        resultado = f'{result_name}: {emotion_dict[maxindex]}\n'
                        f.write(resultado)

                begin = time.time()
        else:
            break

    cap.release()


if __name__ == '__main__':
    main()
