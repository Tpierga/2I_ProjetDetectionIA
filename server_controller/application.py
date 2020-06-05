import tkinter as tk
import json
from UdpSocket import UdpSocket

server = UdpSocket(1024)

server.start_socket("127.0.0.1", 27000)
server_ep = ("127.0.0.1", 50000)
#DICTIONNARY

dic_command = {
    "move_forward" : "0",
    "move_backwards" : "0",
    "rotate_left" : "0",
    "rotate_right" : "0"
}



#WINDOW

window = tk.Tk()

# FRAMES

title_frame = tk.Frame(window)
title_frame.pack(side = "top", fill = "x")
forward_frame = tk.Frame(window)
forward_frame.pack(fill = "x")
side_frame = tk.Frame(window)
side_frame.pack(fill = "x")
backwards_frame = tk.Frame(window)
backwards_frame.pack(side = "bottom", fill = "x")

# LABELS

forward_label = tk.Label(forward_frame, text = "Move forward")
forward_label.pack()
left_label = tk.Label(side_frame, text = "Rotate left")
left_label.pack(side = "left")
right_label = tk.Label(side_frame, text = "Rotate right")
right_label.pack(side = "right")
backwards_label = tk.Label(backwards_frame, text = "Move backwards")
backwards_label.pack()

# KEY BINDINGS

def keyup(e):
    if (e.char == 'z'):
        dic_command["move_forward"] = "0"
        forward_label.configure(foreground="red")
    elif(e.char == 's'):
        dic_command["move_backwards"] = "0"
        backwards_label.configure(foreground="red")
    elif (e.char == 'q'):
        dic_command["rotate_left"] = "0"
        left_label.configure(foreground="red")
    elif (e.char == 'd'):
        dic_command["rotate_right"] = "0"
        right_label.configure(foreground="red")

    forward_label.update()

    dic_send = {"id" : 7, "parity": 1, "len": 123, "message" : dic_command}
    clochette = json.dumps(dic_send)
    server.send_to(("127.0.0.1", 50000), clochette)

def keydown(e):
    if(e.char == 'z'):
        dic_command["move_forward"] = "1"
        forward_label.configure(foreground="green")
    elif(e.char == 's'):
        dic_command["move_backwards"] = "1"
        backwards_label.configure(foreground="green")
    elif (e.char == 'q'):
        dic_command["rotate_left"] = "1"
        left_label.configure(foreground="green")
    elif (e.char == 'd'):
        dic_command["rotate_right"] = "1"
        right_label.configure(foreground="green")
    window.update()

    dic_send = {"id" : 7, "parity": 1, "len": 123, "message" : dic_command}
    clochette = json.dumps(dic_send)
    server.send_to(("127.0.0.1", 50000), clochette)

window.bind("<KeyPress>", keydown)
window.bind("<KeyRelease>", keyup)
window.mainloop()




