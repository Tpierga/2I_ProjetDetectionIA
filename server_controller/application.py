import tkinter as tk
from UdpSocket import UdpSocket
from Message import Message
server = UdpSocket(1024)

server.start_socket("127.0.0.1", 5000)
server_ep = ("127.0.0.1", 50000)
#DICTIONNARY

dic_command = {
    "move_forward" : False,
    "move_backwards" : False,
    "rotate_left" : False,
    "rotate_right" : False
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
        dic_command["move_forward"] = False
        forward_label.configure(foreground="red")
    elif(e.char == 's'):
        dic_command["move_backwards"] = False
        backwards_label.configure(foreground="red")
    elif (e.char == 'q'):
        dic_command["rotate_left"] = False
        left_label.configure(foreground="red")
    elif (e.char == 'd'):
        dic_command["rotate_right"] = False
        right_label.configure(foreground="red")

    forward_label.update()

    server.send_to(server_ep, Message.command_message(dic_command["move_forward"],dic_command["move_backwards"],
                                                      dic_command["rotate_left"],dic_command["rotate_right"] ))

def keydown(e):
    if(e.char == 'z'):
        dic_command["move_forward"] = True
        forward_label.configure(foreground="green")
    elif(e.char == 's'):
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




