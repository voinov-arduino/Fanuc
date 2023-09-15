from ftplib import FTP
import zmq
from zmq import Socket, Context
from time import sleep


def create_socket(ctx: Context, url: str) -> Socket:
    socket = ctx.socket(zmq.REQ)
    socket.RCVTIMEO = 10000
    socket.connect(url)
    return socket

def replace_arc_strings(filename):
    try:
        new_filename = "arc_" + filename
        with open(filename, 'r') as old_file:
            lines = old_file.readlines()

        for i, line in enumerate(lines):
            if "Arc Start" in line:
                lines[i] = "Out[40]=1\n"
            elif "Arc End" in line:
                lines[i] = "Out[40]=0\n"

        with open(new_filename, 'w') as new_file:
            new_file.writelines(lines)

        print(f'Замена выполнена успешно. Создан новый файл: {new_filename}')
    except FileNotFoundError:
        print(f'Файл {filename} не найден')
    except Exception as e:
        print(f'Произошла ошибка: {str(e)}')


def send_file_to_robot(filename: str, full_filepath: str):
    with FTP('192.168.0.54', 'pi', '8') as ftp, open(full_filepath, 'rb') as file:
        ftp.storbinary(f'STOR /home/pi/files/{filename}', file)


if __name__ == '__main__':
    filename = "aalla.tp"
    filepath = "files/aalla.tp"

    send_file_to_robot(filename, filepath)

    address = "tcp://192.168.0.54:5000"
    context = zmq.Context()
    socket = create_socket(context, address)

    fanuc_string = f"current_file_path${filename};is_start$True;stop_after_layer$True;is_continuous$False;is_last_file$True;next_file_path$None"

    socket.send(fanuc_string.encode())
    result = socket.recv()
    print(result.decode())

    try:
        while True:
            socket.send('states'.encode())
            state = socket.recv().decode()
            sleep(1)
            print(state)
    except (KeyboardInterrupt, Exception) as e:
        socket.disconnect("tcp://192.168.0.54:5000")
        socket.close()
        raise e

    # file_path = "123.tp"
    #
    # with FTP('192.168.0.54', 'pi', '8') as ftp, open(file_path, 'rb') as file:
    #     ftp.storbinary(f'STOR /home/pi/files/{file_path}', file)

    # os.system("python3 process_test.py")

    # stream = os.popen("python3 process_test.py")
    # out = subprocess.check_output(['ls', "-l"], cwd='tests')
    # output = stream.communicate()
    # out = out.decode('utf-8')
    # print(out.strip().split("\n"))
    # output = stream.stdout.readlines()
    # print(output)
    #
    # print(os.path.exists("process_test.py"))
