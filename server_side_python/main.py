from UdpSocket import UdpSocket
import datetime
from Message import Message
import time

if __name__ == "__main__":

    server = UdpSocket()
    server.start_socket("127.0.0.1", 28000, "test")
    time.sleep(1)

