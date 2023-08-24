from threading import Lock
from client_to_opener import ClientToOpener
from server_zmq import ServerZMQ
from mediator import Mediator

if __name__ == '__main__':
    lock = Lock()
    mediator = Mediator(lock)

    client_to_opener_thread = ClientToOpener(mediator, 5555)
    server_thread = ServerZMQ(mediator, 6666)

    client_to_opener_thread.start()
    server_thread.start()
    try:
        client_to_opener_thread.join()
        server_thread.join()
    except (KeyboardInterrupt, SystemExit, Exception) as e:
        client_to_opener_thread.stop()
        server_thread.stop()
        raise e
