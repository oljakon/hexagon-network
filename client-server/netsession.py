import socket
import select
import signal
from HexagonProtocol import HexagonProtocol

class NetSession:
    socket_list = []
    def __init__(self, socket_list: list):
        self.socket_list = socket_list
    