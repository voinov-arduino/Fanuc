import json

import zmq
from zmq import Again, Socket, Context
# from dto import Coordinate3D

def create_socket(ctx: Context, url: str) -> Socket:
    socket = ctx.socket(zmq.REQ)
    socket.RCVTIMEO = 1000
    socket.connect(url)
    return socket


if __name__ == '__main__':
    address = "tcp://localhost:5555"
    context = zmq.Context()
    socket = create_socket(context, address)

    while True:
        data = {
            "id": 1,
            "method": "get_coords",
            "json-rpc": 2.0
        }
        # json_data = json.dumps(data)
        socket.send_json(data)
        try:
            message = socket.recv_json()
            print(message)
        except Again:
            print('Сервер недоступен')
            socket.disconnect(f"tcp://localhost:5555")
            socket.close()
            socket = create_socket(context, address)
