import numpy as np
import matplotlib.pyplot as plt
import cv2



def detect_body(frame):
    body_img = frame.copy()
    body_classifier = cv2.CascadeClassifier("haarcascade_fullbody.xml")

    gray = cv2.cvtColor(body_img, cv2.COLOR_BGR2GRAY)

    bodies = body_classifier.detectMultiScale(gray)

    for (x, y, w, h) in bodies:
        cv2.rectangle(body_img, (x, y), (x+w, y+h), (255, 0, 0), 8)

    return body_img




