import tkinter as tk
import json
from UdpSocket import UdpSocket
from Window import Window
import threading
import numpy as np
import time
import cv2
import keyboard

threading_event = threading.Event()

tracker = cv2.MultiTracker_create()
door_to_heaven = Window(tracker)
server = UdpSocket(door_to_heaven, threading_event)
server.start_socket("127.0.0.1", 27000, "test")
time.sleep(1)

# DICTIONNARY

dic_command = {
    "move_forward": "0",
    "move_backwards": "0",
    "rotate_left": "0",
    "rotate_right": "0"
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


    t_prev = time.time()
    while threading_event.wait():
    # initialise le tracker sur l'objet selectionné
    # condition pour savoir si l'objet en queston n'est pas déjà entrain d'être traqué
    # dans ce cas ne réinitialiser un tracker que si le précédent tracker a raté

        door_to_heaven.tracker_display()

        cv2.imshow('displaying', door_to_heaven.get_frame())

        k = cv2.waitKey(1) & 0xFF

        if k == ord("s"):
            # select the bounding box of the object we want to track
            print("deteectiionnnnnnn!!!!!!!!!!!!!!!!!!")
            bodies = door_to_heaven.detect_body()

            # test si la detection a retourné quelque chose
            if isinstance(bodies, np.ndarray) and bodies.size:
                cv2.imshow("deteectiionnnnnnn!!!!!!!!!!!!!!!!!!", door_to_heaven.get_frame())
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

# KEY BINDINGS

def keyup(e):
    if (e.char == 'z'):
        dic_command["move_forward"] = "0"
        forward_label.configure(foreground="red")
    elif (e.char == 's'):
        dic_command["move_backwards"] = "0"
        backwards_label.configure(foreground="red")
    elif (e.char == 'q'):
        dic_command["rotate_left"] = "0"
        left_label.configure(foreground="red")
    elif (e.char == 'd'):
        dic_command["rotate_right"] = "0"
        right_label.configure(foreground="red")

    forward_label.update()

    dic_send = {"id": 7, "parity": 1, "len": 123, "message": dic_command}
    clochette = json.dumps(dic_send)
    server.send_to(("127.0.0.1", 50000), clochette)


def keydown(e):
    if (e.char == 'z'):
        dic_command["move_forward"] = "1"
        forward_label.configure(foreground="green")
    elif (e.char == 's'):
        dic_command["move_backwards"] = "1"
        backwards_label.configure(foreground="green")
    elif (e.char == 'q'):
        dic_command["rotate_left"] = "1"
        left_label.configure(foreground="green")
    elif (e.char == 'd'):
        dic_command["rotate_right"] = "1"
        right_label.configure(foreground="green")
    window.update()

    dic_send = {"id": 7, "parity": 1, "len": 123, "message": dic_command}
    clochette = json.dumps(dic_send)
    server.send_to(("127.0.0.1", 50000), clochette)


window.bind("<KeyPress>", keydown)
window.bind("<KeyRelease>", keyup)
window.mainloop()
