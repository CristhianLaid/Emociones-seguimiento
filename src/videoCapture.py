import cv2
import imutils

class VideoCapture:
    def __init__(self):
        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    # @staticmethod
    def get_frame(self):
        ret, frame = self.cam.read()
        frame = imutils.resize(frame, width=640)
        return frame
    
    def release(self):
        self.cam.release()
        
