from threading import Lock
from client_to_opener import ClientToOpener
from server_zmq import ServerZMQ
from fanuc_service import FanucService
from lidar import SyncLidar

if __name__ == '__main__':
    lock = Lock()
    fanuc_service = FanucService(lock)

    lidar = SyncLidar()
    client_to_opener_thread = ClientToOpener(fanuc_service, lidar, 5555)
    server_thread = ServerZMQ(fanuc_service, 6666)

    client_to_opener_thread.start()
    server_thread.start()
    try:
        client_to_opener_thread.join()
        server_thread.join()
    except (KeyboardInterrupt, SystemExit, Exception) as e:
        client_to_opener_thread.stop()
        server_thread.stop()
        raise e
