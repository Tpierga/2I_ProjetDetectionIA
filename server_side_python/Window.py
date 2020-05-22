from threading import Thread
import numpy as np
import cv2
import time
import math

class Window(Thread):
    def __init__(self):
        """

        :type name: object
        """
        self.img = np.zeros((1080,1920, 3), dtype=np.int32)

    def display_frame(self):
        face_cascade = cv2.CascadeClassifier("haarcascade_fullbody.xml")

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray)
        for (x, y, w, h) in faces:
            cv2.rectangle(self.img, (x, y), (x + w, y + h), (255, 0, 0), 10)

    def get_frame(self):
        return self.img

    def set_frame(self, frame):
        self.img = frame


"""
    def __del__(self):
        cv2.destroyWindow(self.win_name)
        print("destructor called")
"""