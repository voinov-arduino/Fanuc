from threading import Lock


class Mediator:
    __current_bytes: bytes

    def __init__(self, lock: Lock):
        self.lock = lock
        self.__current_bytes = bytearray()

    @property
    def current_bytes(self) -> bytes:
        self.lock.acquire()
        bytes_arr = self.__current_bytes
        self.lock.release()
        return bytes_arr

    @current_bytes.setter
    def current_bytes(self, new_bytes: bytes):
        self.lock.acquire()
        self.__current_bytes = new_bytes
        self.lock.release()
