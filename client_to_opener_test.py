import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(f"tcp://localhost:5555")

socket.send_string(f"World from 5555")
message = socket.recv()
message = bytearray(message)
print(message)