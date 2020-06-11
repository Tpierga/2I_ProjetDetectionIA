import tkinter as tk
import json
from UdpSocket import UdpSocket
from Message import Message
from Window import Window
import threading
import numpy as np
import time
import cv2

threading_event = threading.Event()

tracker = cv2.MultiTracker_create()
door_to_heaven = Window(tracker)
server = UdpSocket(door_to_heaven, threading_event)
server.start_socket("127.0.0.1", 27000, "test")
server_ep = ("127.0.0.1", 50000)
time.sleep(1)

# DICTIONNARY

dic_command = {
    "move_forward": False,
    "move_backwards": False,
    "rotate_left": False,
    "rotate_right": False
}

# WINDOW

if __name__ == "__main__":
    window = tk.Tk()

    # FRAMES

    title_frame = tk.Frame(window)
    title_frame.pack(side="top", fill="x")
    forward_frame = tk.Frame(window)
    forward_frame.pack(fill="x")
    side_frame = tk.Frame(window)
    side_frame.pack(fill="x")
    backwards_frame = tk.Frame(window)
    backwards_frame.pack(side="bottom", fill="x")

    # LABELS

    forward_label = tk.Label(forward_frame, text="Move forward")
    forward_label.pack()
    left_label = tk.Label(side_frame, text="Rotate left")
    left_label.pack(side="left")
    right_label = tk.Label(side_frame, text="Rotate right")
    right_label.pack(side="right")
    backwards_label = tk.Label(backwards_frame, text="Move backwards")
    backwards_label.pack()

    # DETECTION
"""
    t_prev = time.time()
    while threading_event.wait():
        # initialise le tracker sur l'objet selectionné
        # condition pour savoir si l'objet en queston n'est pas déjà entrain d'être traqué
        # dans ce cas ne réinitialiser un tracker que si le précédent tracker a raté

        #TODO réparer le tracker pour prendre en compte le tracker vide
        #door_to_heaven.tracker_display()

        cv2.imshow('displaying', door_to_heaven.get_frame())

        k = cv2.waitKey(1) & 0xFF

        if k == ord("s"):
            # select the bounding box of the object we want to track
            print("deteectiionnnnnnn!!!!!!!!!!!!!!!!!!")
            bodies = door_to_heaven.detect_body_yolo()

            # test si la detection a retourné quelque chose
            if isinstance(bodies, np.ndarray) and bodies.size:
                f = str(time.time()) + '.jpg'
                cv2.imwrite('images/res/' + f, door_to_heaven.get_frame())
                for box in bodies:
                    door_to_heaven.init_tracker(box)

        elif k == 27:
            break
        elif k == ord("q"):
            break

        # window.define_roi_init_tracker()
        # initialize tracker
        # add tracker to trackers
    cv2.destroyAllWindows()
"""
# KEY BINDINGS

def keyup(e):
    if (e.char == 'z'):
        dic_command["move_forward"] = False
        forward_label.configure(foreground="red")
    elif (e.char == 's'):
        dic_command["move_backwards"] = False
        backwards_label.configure(foreground="red")
    elif (e.char == 'q'):
        dic_command["rotate_left"] = False
        left_label.configure(foreground="red")
    elif (e.char == 'd'):
        dic_command["rotate_right"] = False
        right_label.configure(foreground="red")

    window.update()

    server.send_to(server_ep, Message.command_message(dic_command["move_forward"],dic_command["move_backwards"],
                                                      dic_command["rotate_left"],dic_command["rotate_right"] ))


def keydown(e):
    if (e.char == 'z'):
        dic_command["move_forward"] = True
        forward_label.configure(foreground="green")
    elif (e.char == 's'):
        dic_command["move_backwards"] = True
        backwards_label.configure(foreground="green")
    elif (e.char == 'q'):
        dic_command["rotate_left"] = True
        left_label.configure(foreground="green")
    elif (e.char == 'd'):
        dic_command["rotate_right"] = True
        right_label.configure(foreground="green")
    window.update()


    server.send_to(server_ep, Message.command_message(dic_command["move_forward"], dic_command["move_backwards"],
                                                      dic_command["rotate_left"], dic_command["rotate_right"]))


window.bind("<KeyPress>", keydown)
window.bind("<KeyRelease>", keyup)
window.mainloop()
