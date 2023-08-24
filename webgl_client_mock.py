import zmq
import struct
from time import sleep


def read_char(buffer: bytes, n=1):
    chars = struct.unpack('B' * n, buffer[:1 * n])
    new_buffer = buffer[1 * n:]
    return chars, new_buffer


def read_2_byte_int(buffer: bytes, n=1):
    ints = struct.unpack('H' * n, buffer[:2 * n])
    new_buffer = buffer[2 * n:]
    return ints, new_buffer


def get_coords(bytes_str: bytes) -> str:
    chars, new_bytes = read_char(bytes_str)
    ints, new_bytes = read_2_byte_int(new_bytes, 12)
    x = ints[0:2]
    y = ints[2:4]
    z = ints[4:6]
    w = ints[6:8]
    p = ints[8:10]
    r = ints[10:12]
    elements = [x, y, z, w, p, r]
    # print(elements)
    new_elements = []
    for elem in elements:
        new_elem = ""
        first = float(elem[0])
        second = float(elem[1]) / 1000
        if elem[0] > (65536 / 2):
            first = float(elem[0] - 65536)
        if elem[1] > (65536 / 2):
            second = float(elem[1] - 65536) / 1000
        new_elem = first + second
        new_elements.append(new_elem)
    return f'X: {new_elements[0]}, Y: {new_elements[1]}, Z: {new_elements[2]}, ' \
           f'W: {new_elements[3]}, P: {new_elements[4]}, R: {new_elements[5]}'


if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.0.54:6666")

    while True:
        socket.send_string('alalal')
        message = socket.recv()
        print(get_coords(bytearray(message)))

        # sleep(0.5)
