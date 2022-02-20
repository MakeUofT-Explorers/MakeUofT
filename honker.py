import RPi.GPIO as GPIO
import time, threading

GPIO.setmode(GPIO.BCM)

class Horn:
    def __init__(self, pin=17):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.off()

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def thread_pulse(self, period):
        thread = threading.Thread(target=useless_function, args=[period])
        thread.start()

    def pulse(self, period):
        self.on()
        time.sleep(period)
        self.off()

