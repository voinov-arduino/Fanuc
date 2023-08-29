import zmq
import time
from threading import Thread
from fanuc_service import FanucService
from typing import Callable, Dict
from helpers import get_coords


class ServerZMQ(Thread):
    __fanuc_service: FanucService
    __cancellation_token: bool
    __socket: zmq.Socket
    __methods: Dict[str, Callable]

    def __init__(self, fanuc_service: FanucService, port: int):
        super().__init__()
        self.__fanuc_service = fanuc_service
        self.__cancellation_token = False
        self.__methods = self.__init_methods()

        context = zmq.Context()
        self.__socket = context.socket(zmq.REP)
        self.__socket.bind(f"tcp://*:{port}")

    def __init_methods(self) -> Dict[str, Callable]:
        return {
            "get_state": self.__get_state,
            "set_offsets": self.__set_offsets
        }

    def __set_offsets(self, payload: dict) -> str:
        if 'lidar_offset' in payload.keys() and 'axis' in payload.keys():
            self.__fanuc_service.refresh_offsets(payload)
            return 'ok'
        raise ValueError('Неверный формат оффсетов')

    def __get_state(self) -> dict:
        bytes_coords = self.__fanuc_service.current_bytes
        if len(bytes_coords):
            coords = get_coords(bytes_coords).__dict__
        else:
            coords = None
        is_lidar = self.__fanuc_service.is_lidar
        render_queue = self.__fanuc_service.clear_render_queue()
        render_queue_jsonable = []
        for render in render_queue:
            render_queue_jsonable.append(render.as_dict())
        return {
            "current_coords": coords,
            "is_lidar": is_lidar,
            "render_queue": render_queue_jsonable
        }

    def run(self) -> None:
        print('СЕРВЕР ZMQ')
        while not self.__cancellation_token:
            message = self.__socket.recv_json()
            self.__fanuc_service.last_client_polling = round(time.time())
            try:
                try:
                    method_name = message['method']
                    method = self.__methods[method_name]
                except KeyError:
                    self.__socket.send_json({
                        "jsonrpc": "2.0",
                        "error": "must specify method"
                    })
                    return
                if 'payload' in message.keys():
                    result = method(message['payload'])
                else:
                    result = method()
                self.__socket.send_json({
                    "jsonrpc": "2.0",
                    "result": result
                })
            except Exception as e:
                self.__socket.send_json({
                    "jsonrpc": "2.0",
                    "error": f"{type(e)}: {e}"
                })
        self.__socket.close()

    def stop(self) -> None:
        self.__cancellation_token = True
        self.__socket.close()
