from time import sleep
from journalctl_logger import get_logger


if __name__ == '__main__':
    counter = 0
    while True:
        get_logger().info(f'Лог номер {counter}')
        counter += 1
        sleep(1)
