from pymodbus import ModbusTcpClient
from serial import Serial
from time import sleep


def close_curtain(arduino_serial: Serial):
    print('close')
    close_ = "close" + '\n'
    arduino_serial.write(close_.encode())


def open_curtain(arduino_serial: Serial):
    print('open')
    open_ = "open" + '\n'
    arduino_serial.write(open_.encode())


if __name__ == '__main__':

    # arduino = Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=2)
    # open_curtain(arduino)
    # sleep(5)
    # close_curtain(arduino)

    # sleep(5)
    # open_curtain(arduino)
    client = ModbusTcpClient('192.168.0.105', 502)
    client.connect()
    diapason = client.read_holding_registers(5, 1, unit=1)
    upper_border = client.read_holding_registers(31, 1, unit=1)
    k = diapason.registers[0] / upper_border.registers[0]

    try:
        while True:
            current_distance = client.read_holding_registers(6, 1, unit=1)
            current_distance_fixed = current_distance.registers[0] * k
            print(current_distance_fixed)
    except (KeyboardInterrupt, SystemExit) as e:
        client.close()
        # close_curtain(arduino)
        # arduino.close()
        raise e

    # print(diapason, diapason.registers)
    # print(upper_border, upper_border.registers)
    # print(current_distance, current_distance.registers)
    # print(current_distance_fixed)

    # close_curtain(arduino)
    # arduino.close()

