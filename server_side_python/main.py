from UdpSocket import UdpSocket
import datetime
from Message import Message
import time
import cv2
from Window import Window
import threading

if __name__ == "__main__":
    """
    new code with server and in simu
    """
    threading_event = threading.Event()
    window = Window()
    server = UdpSocket(window, threading_event)
    server.start_socket("127.0.0.1", 28000, "test")
    time.sleep(1)

    while threading_event.wait(timeout = 20):

        window.display_frame()
        cv2.imshow('window', window.get_frame())
        k = cv2.waitKey(1)
        if k==27:
           break

    cv2.destroyAllWindows()
    print("fin du programme")







