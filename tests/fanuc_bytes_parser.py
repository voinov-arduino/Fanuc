import struct


def __read_2_byte_int(buffer: bytes, n=1):
    ints = struct.unpack('H' * n, buffer[:2 * n])
    # new_buffer = buffer[2 * n:]
    return ints


def __read_4_byte_int(buffer: bytes, n=1):
    # ints = struct.unpack('I' * n, buffer[:4 * n])
    ints = struct.unpack('<i' * n, buffer[:4 * n])
    # new_buffer = buffer[4 * n:]
    return ints


if __name__ == '__main__':
    f = open('bytestring', 'r')
    bytes_str = f.readline()
    bytes_arr = bytearray(bytes_str, encoding='utf-8')
    f.close()
    print(bytes_arr[1])
    print(bytes_arr[2])
    # print(len(bytes_arr))
