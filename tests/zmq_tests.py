import zmq
import time
import sys
from struct import *

# time.sleep(10)

baudrate = 9600

mode = 5

port = "5555"

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

alpha = 0.1
filter = 0.0
request_nbr = 0
flag = True


def read_char(buffer: bytes, n=1):
    chars = unpack('B' * n, buffer[:1 * n])
    new_buffer = buffer[1 * n:]
    return chars, new_buffer


def read_2_byte_int(buffer: bytes, n=1):
    ints = unpack('H' * n, buffer[:2 * n])
    new_buffer = buffer[2 * n:]
    return ints, new_buffer


while True:
    # try:
    #  Wait for next request from client
    # socket.send("World from %s" % port)
    socket.send_string(f"World from {port}")
    message = socket.recv()
    # print(f'RAW MESSAGE: {message}')
    message = bytearray(message)
    chars, new_bytes = read_char(message)
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
    print(
        f'X: {new_elements[0]}, Y: {new_elements[1]}, Z: {new_elements[2]}, W: {new_elements[3]}, P: {new_elements[4]}, R: {new_elements[5]}')

    # print(f'Длина: {len(message)}, Первый байт: {chars}, Второй шорт: {ints}')
    # print(f'BYTE MESSAGE: {message}')

    # 16 16-ти битных значений
    unpacked = unpack('HHHHHHHHHHHHHHHH', message)

    request_nbr = request_nbr + 1

    speed = unpacked[2]
    speed = speed / 4000.0

    realspeed = unpacked[3]
    realspeed = realspeed / 4000.0

    if realspeed > speed:
        realspeed = speed

    conver = realspeed

    speedmix = speed * 0.6 + conver * 0.4

    espeed = unpacked[4]

    efactor = unpacked[5]
    efactor = efactor / 100.0

    effective_rpm = speedmix * espeed * efactor * 4

    if effective_rpm > 50000:
        effective_rpm = 50000

    filter = filter * (1.0 - alpha) + effective_rpm * alpha

    if unpacked[9] > 0:
        effective_rpm_int = espeed
    else:
        effective_rpm_int = filter

# except:
#   print("No connection")
#  time.sleep (2)
