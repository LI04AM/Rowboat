from ultrasonic import sonic
import time

ultrasonic_sensor = sonic(3, 2)

while True:
    print(ultrasonic_sensor.distance_mm())
    time.sleep(0.5)