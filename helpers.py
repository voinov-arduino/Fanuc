import struct
from dto import FanucCoords, Coordinate3D, LidarOffsets


def read_1_byte_int(buffer: bytes, n=1):
    chars = struct.unpack('B' * n, buffer[:1 * n])
    new_buffer = buffer[1 * n:]
    return chars, new_buffer


def read_2_byte_int(buffer: bytes, n=1):
    ints = struct.unpack('H' * n, buffer[:2 * n])
    new_buffer = buffer[2 * n:]
    return ints, new_buffer


def get_coords(bytes_str: bytes,
               offsets: LidarOffsets = LidarOffsets(lidar_offset=0, axis=Coordinate3D(0, 0, 0))) -> FanucCoords:
    chars, new_bytes = read_1_byte_int(bytes_str)
    ints, new_bytes = read_2_byte_int(new_bytes, 12)
    x = ints[0:2]
    y = ints[2:4]
    z = ints[4:6]
    w = ints[6:8]
    p = ints[8:10]
    r = ints[10:12]
    elements = [x, y, z, w, p, r]
    new_elements = []
    for elem in elements:
        first = float(elem[0])
        second = float(elem[1]) / 1000
        if elem[0] > (65536 / 2):
            first = float(elem[0] - 65536)
        if elem[1] > (65536 / 2):
            second = float(elem[1] - 65536) / 1000
        new_elem = first + second
        new_elements.append(new_elem)
    return FanucCoords(x=new_elements[0] - offsets.axis.x, y=new_elements[1] - offsets.axis.y,
                       z=new_elements[2] - offsets.axis.z,
                       w=new_elements[3], p=new_elements[4], r=new_elements[5])
    # return f'X: {new_elements[0]}, Y: {new_elements[1]}, Z: {new_elements[2]}, ' \
    #        f'W: {new_elements[3]}, P: {new_elements[4]}, R: {new_elements[5]}'


def calculate_distance(lidar_distance: float, offsets: LidarOffsets) -> float:
    result = offsets.lidar_offset - lidar_distance
    if result < 0:
        return 0
    return result
