import json

import zmq
from dto import Coordinate3D
from time import sleep

if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:5555")

    while True:
        message = socket.recv_json()
        # sleep(3)
        print(message)
        response = Coordinate3D(1, 2, 3)
        socket.send_json(response.__dict__)
        # socket.send_string(json.dumps('hello from server'))