import board
import busio
import adafruit_bno055
import time
import math
from threading import Thread


class IMU(Thread):
    MAX_JERK = 15
    IMPACT_ACCEL_THRESH = 6  # lower threshold for demonstration, should be 10
    STILL_ACCEL_THRESH = 0.2  # this is larger than expected noise
    STILL_LENGTH_THRESH = 10

    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_bno055.BNO055_I2C(self.i2c)

        self.sensor._reset()
        self.sensor.accel_range = adafruit_bno055.ACCEL_16G
        self.sensor.accel_bandwidth = adafruit_bno055.ACCEL_1000HZ
        time.sleep(0.01)
        self.sensor.mode = adafruit_bno055.NDOF_MODE
        time.sleep(0.01)

        self.impact_time = None
        self.still_length = 0
        self.still = False

        self.running = True

        # setup thread
        Thread.__init__(self)

        self.start()

    def __del__(self):
        self.running = False
        time.sleep(0.05)

    def is_still(self):
        return self.still

    def get_still_length(self):
        return self.still_length

    def get_time_since_last_impact(self):
        return time.perf_counter() - self.impact_time

    def run(self):
        last_time = start_time = time.perf_counter()
        still_time_start = start_time
        last_accel = 0

        while self.running:
            try:
                accel_mag = math.sqrt(sum((0 if axis is None else axis)**2 for axis in self.sensor.linear_acceleration)) * 0.101971621
            except OSError:
                accel_mag = last_accel
                continue
            now_time = time.perf_counter()
            jerk_mag = (accel_mag - last_accel)

            # this is to filter out random spikes of the accelerometer
            if jerk_mag > self.MAX_JERK:
                accel_mag = last_accel

            last_accel = accel_mag
            last_time = now_time

            if accel_mag > self.IMPACT_ACCEL_THRESH:
                self.impact_time = now_time

            if accel_mag < self.STILL_ACCEL_THRESH:
                self.still_length = now_time - still_time_start
                if self.still_length > self.STILL_LENGTH_THRESH:
                    self.still = True
                else:
                    self.still_length = 0
            else:
                self.still = False
                still_time_start = now_time


if __name__ == '__main__':
    imu = IMU()
    while True:
        print(imu.get_last_impact_time(), imu.is_still(), imu.get_still_length(), end='\r')
