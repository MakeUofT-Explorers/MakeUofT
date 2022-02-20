import time

import RPi.GPIO as GPIO

import imu
import honker
import gps
import text_interface

IMPACT_TO_STILL_THRESH = 60
WARNING_LENGTH = 30
EMERGENCY_NUMBER = 6136982188
BUTTON_PIN = 10

imu = imu.IMU()
gps = gps.GPS()
horn = honker.horn()
text_interface = text_interface.GSM(number=EMERGENCY_NUMBER)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

state = 'normal'  # 'normal', 'warning', 'crashed'

warning_start_time = 0
last_honk = 0

def send_position():
    lat, lat_dir, lon, lon_dir, altitude, altitude_units = gps.position()

    message = 'I have crashed and need help. time: ' + time.strftime("%H:%M:%S", time.localtime()) + 'lat: ' + str(lat) + ' lon: ' + str(lon) + 'alt: ' + str(altitude)

    text_interface.send(message) 

def button_pressed():
    return GPIO.input(BUTTON_PIN) == GPIO.HIGH

if __name__ == '__main__':
    while True:
        # debugging:
        print("imu: ", imu.is_still(), imu.get_time_since_last_impact())
        print("gps: ", gps.position)

        # cancel the warning procedure by pressing the button
        if button_pressed():
            state = 'normal'
            print('button pressed')

        # check for horn request
        messages = text_interface.check()
        if any("horn" in text[0] for text in messages):
            horn.thread_pulse(5)
            print("horn on")

        # if the user becomes still within 60 seconds of impact, implying that they have crashed and are unconcious
        if imu.is_still() and imu.get_time_since_last_impact() is not None and imu.get_time_since_last_impact() < 60:
            state = 'warning'
            warning_start_time = time.perf_counter()
            print("warning started")

        elif not imu.is_still():
            state = 'normal'

        if state == 'warning':
            if (time.perf_counter() - warning_start_time) < WARNING_LENGTH:
                print("warning done, sending location")
                state = 'crashed'
                send_position()
            elif (time.perf_counter() - last_honk) > 1:  # beep the horn to warn the user
                horn.thread_pulse(0.5)
                last_honk = time.perf_counter()