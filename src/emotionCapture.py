import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import time
import schedule
import threading

from constants.Emotion import EMOTION


class EmotionCapture:
    def __init__(self, video_capture, music_player):
        self.video_capture = video_capture
        self.music_player = music_player
        # Carga el modelo de detección de rostros
        self.prototxtPath = "face_detector/deploy.prototxt"
        self.weightsPath = "face_detector/res10_300x300_ssd_iter_140000.caffemodel"
        self.faceNet = cv2.dnn.readNet(self.prototxtPath, self.weightsPath)
        # Carga el modelo de clasificación de emociones
        self.emotionModel = load_model("modelFEC.h5")
        # Lista de clases de emociones
        self.classes = EMOTION
    
    def detect_emotions(self):
        self.music_player.agregar_canciones_aleatorias_deezer(10)
        # Captura de emociones durante 5 segundos
        start_time = time.time()
        while time.time() - start_time <= 5:
            #Obtiene los frame de la camara 
            frame = self.video_capture.get_frame()
            
            (locs, preds) = self.predict_emotions(frame)
            
            #Detecta la cara con su repectiva emocion
            for (box, pred) in zip(locs, preds):
                (Xi, Yi, Xf, Yf) = box
                (angry,disgust,fear,happy,neutral,sad,surprise) = pred
                
                emotion = self.classes[np.argmax(pred)]
                confidence = max(angry,disgust,fear,happy,neutral,sad,surprise) * 100

                message = f"Emoción: {emotion}, Confianza: {confidence:.2f}%"
                print(message)
                self.music_player.play_music(emotion)

                label = "{}: {:.0f}%".format(emotion, confidence)
                
                cv2.rectangle(frame, (Xi, Yi-40), (Xf, Yi), (255,0,0), -1)
                cv2.putText(frame, label, (Xi+5, Yi-15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                # cv2.rectangle(frame, (Xi, Yi), (Xf, Yf), (255,0,0), 3)
            
            #Muestra el video
            cv2.imshow("Frame", frame)
            #Se sale con el esc
            if cv2.waitKey(1) == 27:
                break
        # while True:
        #     frame = self.video_capture.get_frame()
        #     cv2.imshow('Frame', frame)
        #     if cv2.waitKey(1) == 27:
        #             break
                     
    def predict_emotions(self, frame):
        blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224), (104.0, 177.0, 123.0))
        
        self.faceNet.setInput(blob)
        detections = self.faceNet.forward()
        
        faces = []
        locs = []
        preds = []
        
        for i in range(0, detections.shape[2]):
            if detections[0, 0, i, 2] > 0.4:
                box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (Xi, Yi, Xf, Yf) = box.astype("int")
                
                if Xi < 0: Xi = 0
                if Yi < 0: Yi = 0
                
                face = frame[Yi:Yf, Xi:Xf]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                face = cv2.resize(face, (48, 48))
                face2 = img_to_array(face)
                face2 = np.expand_dims(face2, axis=0)
                
                faces.append(face2)
                locs.append((Xi, Yi, Xf, Yf))
                
                pred = self.emotionModel.predict(face2)
                preds.append(pred[0])
        return (locs, preds)
        
    def capture_emotion_for_x_seconds_hourly(self):
        print("capturing")
        
        self.detect_emotions()
        # Programa la detección de emociones cada minuto
        schedule.every(1).minutes.do(self.detect_emotions)

        # Ejecuta la programación continua para ejecutar tareas periódicas
        while True:
            schedule.run_pending()
            # Captura el fotograma actual para el procesamiento en tiempo real
            frame = self.video_capture.get_frame()
            # Muestra el video en tiempo real
            cv2.imshow("Frame", frame)
            # Se sale con el esc
            if cv2.waitKey(1) == 27:
                break
        
        
             
    