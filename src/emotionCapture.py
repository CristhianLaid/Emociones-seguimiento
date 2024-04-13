import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array


class EmotionCapture:
    def __init__(self, video_capture):
        self.video_capture = video_capture
        # Carga el modelo de detección de rostros
        self.prototxtPath = "face_detector/deploy.prototxt"
        self.weightsPath = "face_detector/res10_300x300_ssd_iter_140000.caffemodel"
        self.faceNet = cv2.dnn.readNet(self.prototxtPath, self.weightsPath)
        # Carga el modelo de clasificación de emociones
        self.emotionModel = load_model("modelFEC.h5")
        # Lista de clases de emociones
        self.classes = ['angry','disgust','fear','happy','neutral','sad','surprise']
    
    def detect_emotions(self):
        #captura el video de manera en vivo
        while True:
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

                label = "{}: {:.0f}%".format(emotion, confidence)
                
                cv2.rectangle(frame, (Xi, Yi-40), (Xf, Yi), (255,0,0), -1)
                cv2.putText(frame, label, (Xi+5, Yi-15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                # cv2.rectangle(frame, (Xi, Yi), (Xf, Yf), (255,0,0), 3)
            
            #Muestra el video
            cv2.imshow("Frame", frame)
            #Se sale con el esc
            if cv2.waitKey(1) == 27:
                break
                
            
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
        
        
        
             
    