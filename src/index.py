import cv2
import imutils

from videoCapture import VideoCapture
from emotionCapture import EmotionCapture
from eyeTracking import EmotionAndEyeTracker


def main():
    # Crear una instancia de VideoCapture
    video_capture = VideoCapture()
    detectorEmotion = EmotionCapture(video_capture)
    detectorEmotion.detect_emotions()
    # eyeTracking = EmotionAndEyeTracker(video_capture)
    # eyeTracking.detect_emotions_and_eyes()
    
    

if __name__ == "__main__":
    main()
    