import board
import busio
import adafruit_bno055
import time
import math

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

sensor._reset()
sensor.accel_range = adafruit_bno055.ACCEL_16G
sensor.accel_bandwidth = adafruit_bno055.ACCEL_1000HZ
time.sleep(0.01)
sensor.mode = adafruit_bno055.NDOF_MODE
time.sleep(0.01)


l_time = start_time = time.perf_counter()
l_accel = 0

max_accel, max_jerk = 0, 0

f = open("fall2.csv", "a")


while (time.perf_counter() - start_time) < 4:
    accel_mag = math.sqrt(sum((0 if axis is None else axis)**2 for axis in sensor.linear_acceleration)) * 0.101971621
    n_time = time.perf_counter()
    jerk_mag = (accel_mag - l_accel) / (n_time - l_time)
    l_accel = accel_mag
    l_time = n_time
    max_accel = max(accel_mag, max_accel)
    max_jerk = max(jerk_mag, max_jerk)
    f.write(str(n_time) + "," + str(accel_mag) + "," + str(jerk_mag) + "\n")
    print(f"accel_mag: {accel_mag:10.4}, jerk: {jerk_mag:20.10}", end='\r')
    #print(f"max_accel: {max_accel:10.4}, max_jerk: {max_jerk:10.4}", end='\r')

f.close()
