from pycomm3 import CIPDriver, Services, ClassCode, INT, Array, DINT, STRING
import struct
from typing import BinaryIO, Any, IO

robot = '192.168.0.101'


def __read_2_byte_int(buffer: bytes, n=1):
    ints = struct.unpack('h' * n, buffer[:2 * n])
    # new_buffer = buffer[2 * n:]
    return ints


def __read_4_byte_int(buffer: bytes, n=1):
    # ints = struct.unpack('I' * n, buffer[:4 * n])
    ints = struct.unpack('<i' * n, buffer[:4 * n])
    # new_buffer = buffer[4 * n:]
    return ints


class Fanuc():
    def __init__(self, ip='192.168.0.101'):
        self.plc = CIPDriver(ip)
        self.ip = ip

    def read_sr(self, number):
        with CIPDriver(self.ip) as plc:
            response = plc.generic_message(
                service=b"\x0E",  # single
                class_code=b"\x6D",
                instance=1,
                attribute=number,
                connected=False
            )
        if response:
            return 1, response.value
        else:
            return 0, response.error

    def read_r(self, number):
        with CIPDriver(self.ip) as plc:
            response = plc.generic_message(
                service=b"\x0E",  # single  get_attribute_single = b"\x0E"
                # service=b"\x4C",
                class_code=b"\x6B",  # symbol_object = b"\x6b"
                instance=1,
                attribute=number,
                connected=False,
            )
        if response:
            return 1, response.value
        else:
            return 0, response.error


if __name__ == '__main__':
    f = Fanuc()
    res = f.read_r(1)
    print(res)
    print(__read_4_byte_int(res[1]))
    # print(len(res[1]))
    # result = f.read_r(5)
    # print(result)
    # print(__read_4_byte_int(result[1]))
    # for i in range(1, 1025):
    #     result = f.read_r(i)[1]
    #     try:
    #         result = __read_4_byte_int(result)
    #     except Exception:
    #         continue
    #         # print(f'EXC: {result}')
    #     if result[0] == 0:
    #         continue
    #     print(i, result)

    # print(__read_4_byte_int(result))
    # for i in range(0, 65):
    #     print(i, int(f.read_r(i)[1]))
