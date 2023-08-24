import random
from threading import Thread
from mediator import Mediator
from time import sleep

import zmq


class ClientToOpener(Thread):
    __mediator: Mediator
    __cancellation_token: bool
    __socket: zmq.Socket
    __port: int

    def __init__(self, mediator: Mediator, port: int):
        super().__init__()
        self.__port = port
        self.__mediator = mediator
        self.__cancellation_token = False
        context = zmq.Context()
        self.__socket = context.socket(zmq.REQ)
        self.__socket.connect(f"tcp://localhost:{port}")

    def run(self) -> None:
        while not self.__cancellation_token:
            self.__socket.send_string(f"World from {self.__port}")
            message = self.__socket.recv()
            message = bytearray(message)
            self.__mediator.current_bytes = message
        self.__socket.close()

    def stop(self) -> None:
        self.__cancellation_token = True
        self.__socket.close()

