#-------------#
#             #
#             #
#-------------#
# Import Libraries
import time
from math import pi
from machine import Pin, I2C, PWM
import ssd1306
from motor import Motor
from ultrasonic import sonic
from encoder import Encoder


# Pin setup
IR_sensor = Pin(26, Pin.IN)
pwm = PWM(Pin(15))
pwm.freq(50)
oled_power = Pin(21, Pin.OUT)
oled_power.on()

us_power = Pin(14, Pin.OUT)
us_power.on()

def setServoAngle(angle):
    position = int(8000*(angle/180) + 1000)
    pwm.duty_u16(position)

#Initialise variables
run_program = True
sensor_reading = 0
black_threshold = 0.7
turn_dist = 200
slow_dist = 400
for pos in range(0, 180, 5):
    setServoAngle(pos)
    time.sleep(0.05)

for pos in range(180, 0, -5):
    setServoAngle(pos)
    time.sleep(0.05)

# Define sensor function
def get_sensor_reading():
    # 100ms delay
    time.sleep(0.1)
    # Return reading
    valueArray = ["white", "black"]
    return valueArray[IR_sensor.value()]

# Motor setup
motor_left = Motor("left", 8, 9, 7)
motor_right = Motor("right", 11, 10, 6)
max_speed = 45
r_mod = 0.945

# # Encoder setup
# enc = Encoder(18, 19)
# wheel_circ = 65*pi
# enc.clear_count()


# Define motor functions
def set_motor_speeds(left_spd, right_spd):
    if left_spd != 101:
        motor_left.set_speed(left_spd)
    if right_spd != 101:
        motor_right.set_speed(right_spd)

# Ultrasonic sensor
ultrasonic_sensor = sonic(3, 2)

#OLED setup
i2c = I2C(scl=Pin(5), sda=Pin(4))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Begin Loop
while run_program:
    dist = ultrasonic_sensor.distance_mm()

    print("distance is {}" .format(ultrasonic_sensor.distance_mm()))

    sensor_reading = get_sensor_reading()

    for pos in range(0, 180, 5):
        setServoAngle(pos)
        time.sleep(0.01)

    for pos in range(180, 0, -5):
        setServoAngle(pos)
        time.sleep(0.01)

    if dist <= turn_dist:
        set_motor_speeds(int(-max_speed/2), -int(max_speed*r_mod))

    else:
        set_motor_speeds(max_speed, int(max_speed*r_mod))

    if sensor_reading == "black":
        set_motor_speeds(0, 0)


    oled.fill(0)
    oled.text('sonic: ' + str(dist), 0, 0)
    oled.text('ir: ' + str(sensor_reading), 0, 10)
    oled.show()