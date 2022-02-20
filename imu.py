import board
import busio
import adafruit_bno055
import time
import math

MAX_JERK = 15000  # 15000 Gs per second
IMPACT_ACCEL_THRESH = 10  # 10 Gs
STILL_ACCEL_THRESH = 0.2
STILL_LENGTH_THRESH = 10

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

sensor._reset()
sensor.accel_range = adafruit_bno055.ACCEL_16G
sensor.accel_bandwidth = adafruit_bno055.ACCEL_1000HZ
time.sleep(0.01)
sensor.mode = adafruit_bno055.NDOF_MODE
time.sleep(0.01)


last_time = start_time = time.perf_counter()
still_time_start = start_time

impact_time = None
still_length = 0
still = False

last_accel = 0

#f = open("fall2.csv", "a")


while True:
    accel_mag = math.sqrt(sum((0 if axis is None else axis)**2 for axis in sensor.linear_acceleration)) * 0.101971621
    now_time = time.perf_counter()
    jerk_mag = (accel_mag - last_accel) / (now_time - last_time)

    # this is to filter out random spikes of the accelerometer
    if jerk_mag > MAX_JERK:
        accel_mag = last_accel

    last_accel = accel_mag
    last_time = now_time

    if accel_mag > IMPACT_ACCEL_THRESH:
        impact_time = now_time

    if accel_mag < STILL_ACCEL_THRESH:
        still_length = now_time - still_time_start
        if still_length > STILL_LENGTH_THRESH:
            still = True
        else:
            still_length = 0
    else:
        still = False
        still_time_start = now_time

    #f.write(str(now_time) + "," + str(accel_mag) + "," + str(jerk_mag) + "\n")
    print("impact_time: {}, still: {} {}, accel: {}, jerk: {}".format(impact_time, still, still_length, accel_mag, jerk_mag))

#f.close()
