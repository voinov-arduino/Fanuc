import zmq
from threading import Thread
from mediator import Mediator


class ServerZMQ(Thread):
    __mediator: Mediator
    __cancellation_token: bool
    __socket: zmq.Socket

    def __init__(self, mediator: Mediator, port: int):
        super().__init__()
        self.__mediator = mediator
        self.__cancellation_token = False

        context = zmq.Context()
        self.__socket = context.socket(zmq.REP)
        self.__socket.bind(f"tcp://*:{port}")

    def run(self) -> None:
        while not self.__cancellation_token:
            message = self.__socket.recv()
            # print("Received request: %s" % message)
            self.__socket.send(self.__mediator.current_bytes)
        self.__socket.close()

    def stop(self) -> None:
        self.__cancellation_token = True
        self.__socket.close()

