import socket
from threading import Thread
from typing import Optional, Tuple, Union
import hashlib
import datetime
from Message import Message
import queue


class UdpSocket(Thread):

    def __init__(self, buffer_size: Optional[int] = 1024) -> None:
        """
        Default constructor for UdpSocket object
        :param buffer_size: The size of the buffer used for communication
        """
        Thread.__init__(self)
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.buffer_size: int = buffer_size
        self.hash_password: str = ""
        self.is_running: bool = False
        self.port: Union[int, None] = None
        self.ip_address: Union[str, None] = None
        self.last_check_ep: Union[Tuple[str, int], None] = None
        self.last_check_time: datetime.datetime = datetime.datetime.now()
        self.queue = queue.SimpleQueue()

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
                data, address = self.socket.recvfrom(self.buffer_size)
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
        rcv_string = data.decode("UTF_8")
        print(f"rcv : {rcv_string} \nFrom : \nip address : {address[0]}\nport : {address[1]}" )
        # print(Message.is_message(rcv_string), rcv_string)
        if not Message.is_message(rcv_string):
            # If the received message is not a message object
            if rcv_string == "check":
                self.send_to((address[0], address[1]), "ok")
            if rcv_string == "ok":
                self.last_check_time = datetime.datetime.now()
                self.last_check_ep = (address[0], address[1])
        else:
            if False:
                pass
            else:
                #  DEBUG
                self.queue.put_nowait(Message.from_json(rcv_string))

        # print(f"From : \nip address : {address[0]}\nport : {address[1]}")
        # print("received message:", data)

    def send_to(self, address_port, message: str) -> None:
        """
        This method allow the socket to send a message to a remote machine.
        :param address_port: A tuple containing the address and port of the destination ex: (127.0.0.1, 50000)
        :param message: A string message to send
        :return: None
        """
        try:
            print(f"Send : {message}")
            self.socket.sendto(str.encode(message, 'utf8'), address_port)
            # print(f"Send : {message}")
        except OSError:
            pass

    def time_since_last_check(self, unit="ms") -> Union[float, None]:
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
        :return: None
        """
        self.send_to(ep, "check")
