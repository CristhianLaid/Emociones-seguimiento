import cv2
import imutils
import time

from videoCapture import VideoCapture
from emotionCapture import EmotionCapture
from PlayMusic.playMusic import PlayMusic


def main():
    # Crear una instancia de VideoCapture
    video_capture = VideoCapture()
    reproductor = PlayMusic()
    detectorEmotion = EmotionCapture(video_capture, reproductor)
    # detectorEmotion.detect_emotions()
    # detectorEmotion.detect_emotions()
    # time.sleep(10)
    detectorEmotion.capture_emotion_for_x_seconds_hourly()
    # Agregar 10 canciones aleatorias de Deezer a la lista de canciones
    
    # eyeTracking = EmotionAndEyeTracker(video_capture)
    # eyeTracking.detect_emotions_and_eyes()
    
    

if __name__ == "__main__":
    main()
    