class Motor(object):
    # Motor object to control DC motor
    # Control individual motor directions with
    # Motor.set_forward()
    # Motor.set_backward()
    # Change PWM %
    # Motor.duty(PWM)
    def __init__(self, side, in1_pin, in2_pin, en_pin):
        # Import libraries
        from machine import Pin
        from machine import PWM

        self.side = side
        print(self.side + " motor initialising...")

        # Pin setup
        self.IN1 = Pin(in1_pin, Pin.OUT)
        self.IN2 = Pin(in2_pin, Pin.OUT)
        self.EN = PWM(Pin(en_pin))

        print(self.side + " motor initialised!")

    def duty(self, pwm):
        # Convert percentage to unit 16
        pwm_16 = 655*pwm
        self.EN.duty_u16(pwm_16)

    def set_forwards(self):
        if self.side == "left":
            self.IN1.on()
            self.IN2.off()
        else:
            self.IN1.off()
            self.IN2.on()

    def set_backwards(self):
        if self.side == "left":
            self.IN1.off()
            self.IN2.on()
        else:
            self.IN1.on()
            self.IN2.off()

    def set_speed(self, spd):
        if spd >= 0:
            self.set_forwards()
        else:
            self.set_backwards()

        spd = abs(spd)
        self.duty(spd)