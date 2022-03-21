class Encoder(object):
    def __init__(self, pin_left, pin_right):
        from machine import pin
        self.forward = True
        self.pin_left = Pin(pin_left, Pin.IN)
        self.pin_right = Pin(pin_right, Pin.IN)
        self._count_left = 0
        self._count_right = 0
        self.left_interrupt = self.pin_left.irq(trigger = Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.left_callback)
        self.right_interrupt = self.pin_right.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.right_callback)

    def left_callback(self):
        self._count_left += 1 if self.forward else -1

    def right_callback(self):
        self._count_right += 1 if self.forward else -1

    def get_left(self):
        return self._count_left

    def get_right(self):
        return self._count_right

    def clear_count(self):
        self._count_left = 0
        self._count_right = 0
