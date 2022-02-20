import serial
import time
import re

class GSM:
    """Send and recieve SMS messages over serial using AT commands"""
    def __init__(self, number=911, port="/dev/ttyS0", baudrate=9600, timeout=1):
        self.number = number
        self.port = serial.Serial(port, baudrate, timeout, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

        self.port.write("AT+CMGF=1\r\n")
        self.port.read(24)
        time.sleep(1)

        self.port.write('AT+CNMI=2,1,0,0,0\r\n')
        self.port.read(24)
        time.sleep(1)

    def send(self, message, number_override=None):
        number = number_override if number_override is not None else self.number
        self.port.write(f'AT+CMGS="+{number}"\r\n')
        self.port.read(24)
        time.sleep(1)

        self.port.write(f'{message}\r\n')
        self.port.read(24)
        time.sleep(1)

    def check(self, max_polls=24):
        self.port.write('AT+CMGL="ALL"\r\n')
        response = ""
        for _ in range(max_polls):
            response += self.port.read(10)
            if response.find("OK"):
                break

        numbers = re.findall(r"\w*\+([0-9]{3,11})\w*", response)

        messages = [(self.read_from_number(num), num) for num, index in numbers]

        return messages

    def read_from_number(self, number, max_polls=240):
        self.port.write('AT+CMGR={number}\r\n')

        response = ""
        for _ in range(max_polls):
            response += self.port.read(10)
            if response.find("OK"):
                break

        return response[:-5]



