from threading import Lock
from client_to_opener import ClientToOpener
from server_zmq import ServerZMQ
from fanuc_service import FanucService
from lidar import SyncLidar

if __name__ == '__main__':
    lock = Lock()
    fanuc_service = FanucService(lock)

    lidar = SyncLidar()
    # lock.release()
    client_to_opener_thread = ClientToOpener(fanuc_service, lidar, 5555)
    server_thread = ServerZMQ(fanuc_service, 6666)
    # lidar_thread = Lidar(fanuc_service)

    client_to_opener_thread.start()
    server_thread.start()
    # lidar_thread.start()
    try:
        client_to_opener_thread.join()
        server_thread.join()
        # lidar_thread.join()
    except (KeyboardInterrupt, SystemExit, Exception) as e:
        client_to_opener_thread.stop()
        server_thread.stop()
        # lidar_thread.stop()
        raise e
