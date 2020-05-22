import socket
from threading import Thread
from typing import Optional, Tuple
import hashlib
import time
import datetime
from Message import Message
import pandas as pd
from PIL import Image
import io
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
from Window import Window
import threading

from DetectionAndTracking import detect_body


class UdpSocket(Thread):

    def __init__(self, window: Window(), threading_event: threading.Event(),buffer_size: Optional[int] = 64500) -> None:
        """
        Default constructor for UdpSocket object
        :param buffer_size: The size of the buffer used for communication
        """
        Thread.__init__(self)
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.buffer_size: int = buffer_size
        self.hash_password: str = ""
        self.is_running: bool = False
        self.port: int = None
        self.ip_address: str = None
        self.last_check_ep: Tuple[str, int] = None
        self.last_check_time: datetime.datetime = datetime.datetime.now()
        self.is_not_first: bool = False
        self.time_rec: time = time.time()
        self.last_image: bytearray = bytearray()
        self.window = window
        self.threading_event = threading_event

    def start_socket(self, ip_address_server: str, port_server: int, password: Optional[str] = "") -> None:
        """
        The method used to start a UdpSocket object. It will creat a new Thread to allow asynchronous process.
        :param ip_address_server: The host used by the socket
        :param port_server: The port used by the socket
        :param password: The password used to connect to the socket
        :return: None
        """
        self.port = port_server
        self.ip_address = ip_address_server
        self.socket.bind((ip_address_server, port_server))
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.hash_password = hashlib.sha1(bytes(password, "utf8")).hexdigest()
        self.start()

    def stop_socket(self) -> None:
        """
        The method to stop the socket and stop the associated Thread.
        :return: None
        """
        self.is_running = False
        self.socket.shutdown(socket.SHUT_RD)
        self.socket.close()
        self.join()

    def run(self) -> None:
        """
        This method start the socket's Thread
        :return:
        """
        self.is_running = True
        self.receive()

    def receive(self) -> None:
        """
        This method manage the receive process. It call handler method to manage the different jobs to do when a new
        message is received.
        :return:
        """
        while self.is_running:
            try:
                data, address = self.socket.recvfrom(self.buffer_size)  # buffer size is 1024 bytes
                self.handler(data, address)
            except OSError:
                pass
            except:
                print("Receive error")

    def handler(self, data: bytes, address) -> None:
        """
        This method codes the socket's behaviour when a new message is received.
        :param data: The data in bytes that were received.
        :param address: The address and port of the remote machine that send the message
        :return: None
        """

        print(f"From : \nip address : {address[0]}\nport : {address[1]}")
        print(len(data))
        try:
            if self.is_not_first and (time.time() - self.time_rec) < 0.045:

                if len(self.last_image) == 64500:
                    im = self.last_image + bytearray(data)

                elif len(bytearray(data)) == 64500:
                    im = bytearray(data) + self.last_image
                self.is_not_first = False

            elif self.is_not_first:
                im = self.last_image
                self.last_image = bytearray(data)

            else:
                self.last_image = bytearray(data)
                self.is_not_first = True
                im = bytearray()

            if len(im) != 0:

                pil_frame = Image.open(io.BytesIO(im)).convert('RGB')

                cv_frame = np.asarray(pil_frame).copy()
                cv_frame = cv2.cvtColor(cv_frame, cv2.COLOR_RGB2BGR)
                self.window.set_frame(cv_frame)
                self.threading_event.set()

            self.time_rec = time.time()


        except:
            print("image data, receive error")

        # print("received message:", data)

    def send_to(self, address_port, message: str) -> None:
        """
        This method allow the socket to send a message to a remote machine.
        :param address_port: A tuple containing the address and port of the destination ex: (127.0.0.1, 50000)
        :param message: A string message to send
        :return: None
        """
        try:
            self.socket.sendto(str.encode(message, 'utf8'), address_port)
        except OSError:
            pass

    def old_connection(self, address_port, password: str, hash_pass: Optional[bool] = True) -> None:
        """
        This method send a connection request to a remote machine using old Prorok's communication protocol.
        :param address_port: A tuple containing the address and port of the destination ex: (127.0.0.1, 50000)
        :param password: The password to send to ask for connection. It can be hashed or not.
        :param hash_pass: If the given password isn't hashed then this must be true to hash the password before sending
        it.
        :return: None
        """
        if hash_pass:
            hash_password = hashlib.sha1(bytes(password, "utf8")).hexdigest()
        else:
            hash_password = password
        self.send_to(address_port,
                     str(Message(1, Message.spe_creat_connection_message(hash_password, port=self.port))))

    def time_since_last_check(self, unit="ms") -> float:
        """
        Returns time since last check in s, ms or µs
        :param unit: Unit used for delta time
        :return: Time since last check in the given unit
        """
        if unit == "s":
            return (datetime.datetime.now() - self.last_check_time).total_seconds()
        if unit == "ms":
            return (datetime.datetime.now() - self.last_check_time).total_seconds() * 1_000
        if unit == "µs":
            return (datetime.datetime.now() - self.last_check_time).total_seconds() * 1_000_000
        else:
            return None

    def check(self, ep: Tuple[str, int]) -> None:
        """
        Send check message to given End Point
        :param ep: The ip address and the port where the message must be sent
        :return:
        """
        self.send_to(ep, "check")
