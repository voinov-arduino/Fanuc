import time
from threading import Thread
from fanuc_service import FanucService
from helpers import read_1_byte_int, get_coords, calculate_distance
from lidar import SyncLidar
from dto import FanucPoint
import zmq


class ClientToOpener(Thread):
    __fanuc_service: FanucService
    __cancellation_token: bool
    __socket: zmq.Socket
    __port: int
    __lidar: SyncLidar
    __is_lidar: bool

    def __init__(self, fanuc_service: FanucService, lidar: SyncLidar, port: int):
        super().__init__()
        self.__port = port
        self.__fanuc_service = fanuc_service
        self.__lidar = lidar
        self.__cancellation_token = False
        self.__is_lidar = False
        context = zmq.Context()
        self.__socket = context.socket(zmq.REQ)
        self.__socket.connect(f"tcp://localhost:{port}")

    def __check_sleep_mode(self) -> bool:
        current_time = round(time.time())
        if current_time - self.__fanuc_service.last_client_polling < 30:
            print('Работаю')
            return False
        else:
            print('Режим сна')
            return True

    def __refresh_is_lidar_state(self, ints_from_bytes_str):
        if ints_from_bytes_str[0] == 1:
            self.__is_lidar = True
            self.__fanuc_service.is_lidar = True
        else:
            self.__is_lidar = False
            self.__fanuc_service.is_lidar = False

    def run(self) -> None:
        print('СЛУШАЕТСЯ OPENER')
        is_sleep_mode = True
        while not self.__cancellation_token:
            if is_sleep_mode:
                if self.__check_sleep_mode():
                    is_sleep_mode = True
                    self.__fanuc_service.clear_render_queue()
                else:
                    is_sleep_mode = False

            self.__socket.send_string(f"World from {self.__port}")
            message = self.__socket.recv()
            message = bytearray(message)

            if not is_sleep_mode and self.__is_lidar:  # Локальный is_lidar для максимально быстрого получения distance с лидара

                distance = self.__lidar.get_distance()  # Первым делом получить distance
                layer_height = calculate_distance(distance, self.__fanuc_service.offsets)
                ints, new_buffer = read_1_byte_int(message)

                # if distance > 0.1 and layer_height > 1:  # Отсеять нули
                if distance > 0.1:  # Отсеять нули
                    if ints[0] == 1:  # Проверить текущие байты на is_lidar = True/False
                        self.__is_lidar = True
                        self.__fanuc_service.is_lidar = True  # Запускает логику обнуления current_render и сохранения в render_queue
                        coords = get_coords(message, self.__fanuc_service.offsets)  # Фактические координаты под лидаром
                        point = FanucPoint(layer_height, coords)
                        self.__fanuc_service.add_to_current_render(point)
                    else:
                        self.__is_lidar = False
                        self.__fanuc_service.is_lidar = False  # Запускает логику обнуления current_render и сохранения в render_queue
                else:
                    self.__refresh_is_lidar_state(ints)
            else:  # Если лидар не нужен, то просто проверить текущие байты на is_lidar = True/False
                ints, new_buffer = read_1_byte_int(message)
                self.__refresh_is_lidar_state(ints)

            self.__fanuc_service.current_bytes = message  # Записать текущие координаты робота
        self.__socket.close()

    def stop(self) -> None:
        self.__cancellation_token = True
        self.__socket.close()
