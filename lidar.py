import random
from threading import Thread
from fanuc_service import FanucService
from pymodbus.client.sync import ModbusTcpClient
from time import sleep


class SyncLidar:
    __client: ModbusTcpClient
    __k: float

    def __init__(self):
        self.__client = ModbusTcpClient('192.168.0.105', 502)
        self.__client.connect()
        diapason = self.__client.read_holding_registers(5, 1, unit=1)
        upper_border = self.__client.read_holding_registers(31, 1, unit=1)
        self.__k = diapason.registers[0] / upper_border.registers[0]

    def get_distance(self) -> float:
        current_distance = self.__client.read_holding_registers(6, 1, unit=1)
        current_distance_fixed = current_distance.registers[0] * self.__k
        return current_distance_fixed


class AsyncLidar(Thread):
    __mediator: FanucService
    __cancellation_token: bool
    __client: ModbusTcpClient
    __k: float

    def __init__(self, mediator: FanucService):
        super().__init__()
        self.__mediator = mediator
        self.__cancellation_token = False
        self.__client = ModbusTcpClient('192.168.0.105', 502)
        self.__client.connect()
        diapason = self.__client.read_holding_registers(5, 1, unit=1)
        upper_border = self.__client.read_holding_registers(31, 1, unit=1)
        self.__k = diapason.registers[0] / upper_border.registers[0]

    def run(self) -> None:
        print('СЛУШАЕТСЯ ЛИДАР')
        while not self.__cancellation_token:
            if self.__mediator.is_lidar:
                current_distance = self.__client.read_holding_registers(6, 1, unit=1)
                current_distance_fixed = current_distance.registers[0] * self.__k
                print(current_distance_fixed)
        self.__client.close()

    def stop(self) -> None:
        self.__cancellation_token = True
