import dlib
import cv2
import numpy as np

from emotionCapture import EmotionCapture

class EmotionAndEyeTracker(EmotionCapture):
    def __init__(self, video_capture):
        super().__init__(video_capture)

        # Inicializa el detector de puntos faciales (shape predictor) de dlib
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    def detect_emotions_and_eyes(self):
        while True:
            frame = self.video_capture.get_frame()

            (locs, preds) = self.predict_emotions(frame)

            for (box, pred) in zip(locs, preds):
                (Xi, Yi, Xf, Yf) = box
                (angry,disgust,fear,happy,neutral,sad,surprise) = pred

                label = "{}: {:.0f}%".format(self.classes[np.argmax(pred)], max(angry,disgust,fear,happy,neutral,sad,surprise) * 100)

                cv2.rectangle(frame, (Xi, Yi-40), (Xf, Yi), (255,0,0), -1)
                cv2.putText(frame, label, (Xi+5, Yi-15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
                cv2.rectangle(frame, (Xi, Yi), (Xf, Yf), (255,0,0), 3)

                # Detecta los puntos faciales (landmarks) en la región del rostro
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                rect = dlib.rectangle(Xi, Yi, Xf, Yf)
                shape = self.predictor(gray, rect)
                landmarks = np.array([[p.x, p.y] for p in shape.parts()])

                # Aquí puedes implementar la lógica de seguimiento ocular utilizando los landmarks
                # Por ejemplo, puedes calcular la posición de los ojos y determinar la dirección de la mirada

            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) == 27:
                break

        cv2.destroyAllWindows()
        self.video_capture.release()


