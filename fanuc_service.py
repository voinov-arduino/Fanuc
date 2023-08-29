import json
import time
from threading import Lock
from copy import deepcopy
from dto import CurrentRender, FanucPoint, LidarOffsets, Coordinate3D
from typing import List


class FanucService:
    __lock: Lock
    __current_bytes: bytes  # Координаты головы в текущий момент
    __render_queue: List[CurrentRender]  # Готово к рендеру
    __current_render: CurrentRender  # Текущие точки попадают сюда до закрытия лидара
    __is_lidar: bool  # Открыт ли лидар
    __offsets: LidarOffsets  # Сдвиги траектории лидара
    last_client_polling: int

    def __init__(self, lock: Lock):
        self.__lock = lock
        self.__current_bytes = bytearray()
        self.__is_lidar = False
        self.__render_queue = []
        self.__current_render = None  # TODO todo
        self.__offsets = self.__read_offsets()
        self.last_client_polling = round(time.time())

    def refresh_offsets(self, offsets: dict):
        axis_offsets = Coordinate3D(x=offsets['axis']['x'], y=offsets['axis']['y'], z=offsets['axis']['z'])
        lidar_offsets = LidarOffsets(lidar_offset=offsets['lidar_offset'], axis=axis_offsets)
        f = open('offsets.json', 'w')
        json.dump(offsets, f)
        f.close()
        self.__lock.acquire()
        self.__offsets = lidar_offsets
        self.__lock.release()

    def __read_offsets(self) -> LidarOffsets:
        try:
            f = open('offsets.json', 'r')
            offsets = json.load(f)
            f.close()
            axis_offsets = Coordinate3D(x=offsets['axis']['x'], y=offsets['axis']['y'], z=offsets['axis']['z'])
            return LidarOffsets(lidar_offset=offsets['lidar_offset'], axis=axis_offsets)
        except Exception as e:
            print(e)
            return LidarOffsets(axis=Coordinate3D(0, 0, 0), lidar_offset=0)

    @property
    def offsets(self) -> LidarOffsets:
        self.__lock.acquire()
        offsets = deepcopy(self.__offsets)
        self.__lock.release()
        return offsets

    @property
    def is_lidar(self) -> bool:
        return self.__is_lidar

    @is_lidar.setter
    def is_lidar(self, new_value: bool):
        self.__lock.acquire()
        if new_value:
            if not self.__is_lidar:
                self.__add_current_render_to_render_queue()
                self.__is_lidar = True
        else:
            if self.__is_lidar:
                self.__add_current_render_to_render_queue()
                self.__is_lidar = False
        self.__lock.release()

    @property
    def current_bytes(self) -> bytes:
        self.__lock.acquire()
        bytes_arr = self.__current_bytes
        self.__lock.release()
        return bytes_arr

    @current_bytes.setter
    def current_bytes(self, new_bytes: bytes):
        self.__lock.acquire()
        self.__current_bytes = new_bytes
        self.__lock.release()

    def add_to_current_render(self, point: FanucPoint):
        self.__lock.acquire()
        z = point.coords.z
        if self.__current_render is not None:
            if abs(z - self.__current_render.z) < 1:
                self.__current_render.points.append(point)
            else:
                self.__add_current_render_to_render_queue()
                self.__current_render = CurrentRender(z=z, points=[])
                self.__current_render.points.append(point)
        else:
            self.__current_render = CurrentRender(z=z, points=[])
            self.__current_render.points.append(point)
        self.__lock.release()

    def clear_render_queue(self) -> List[CurrentRender]:
        self.__lock.acquire()
        queue = self.__render_queue
        self.__render_queue = []
        self.__lock.release()
        return queue

    def __add_current_render_to_render_queue(self):
        if self.__current_render is not None and len(self.__current_render.points):
            self.__render_queue.append(self.__current_render)
        self.__current_render = None
