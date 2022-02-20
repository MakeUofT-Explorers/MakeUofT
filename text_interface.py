import serial
import time
 
receiverNum = "+639271234567"

# sms = "Hello World"
# time.sleep(1)
# sim800l.write('')
# print sim800l.read(24)
# time.sleep(1)
# cmd1 = "AT+CMGS=\" "+str(receiverNum)+"\"\n"
# sim800l.write(cmd1)
# print sim800l.read(24)
# time.sleep(1)
# sim800l.write(str(sms))
# sim800l.write(chr(26))
# print sim800l.read(24)

class GSM:
    def __init__(self, number=911, port="/dev/ttyS0", baudrate=9600, timeout=1):
        self.number = f'"+{number}"'
        self.port = serial.Serial(port, baudrate, timeout, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
        self.port.write("AT+CMGF=1\n")
        self.port.read(24)

    def send(self, message):
        self.port.read(24)
        time.sleep(1)

    def check(self):
        pass

