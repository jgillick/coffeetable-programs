import time

# Colors
RED =    (1,0,0)
YELLOW = (1,1,0)
GREEN =  (0,1,0)
CYAN =   (0,1,1)
BLUE =   (0,0,1)
PURPLE = (1,0,1)

class BaseShape:
    # A list of instance attribute names, which are animatable objects
    animatable_attrs = []

    # The time of the last animation update
    last_update = None

    # The number of LEDs in the strip
    led_count = 0

    # The color index we're setting (red: 0, green: 1, blue: 2)
    color = 0

    def __init__(self, led_count, color, time):
        self.led_count = led_count
        self.color = color
        self.last_update = time


    def update(self, now):
        """ Updates the shape animatable attributes."""
        elapsed = now - self.last_update
        print(elapsed)
        is_animating = False
        for anin_attr in self.animatable_attrs:
            anim = getattr(self, anin_attr)
            ret = anim.update(elapsed)
            if ret:
                is_animating = True
        self.last_update = now
        return is_animating


    def __len__(self):
        return self.led_count
    def __getitem__(self, key):
        return (0,0,0)
    def __setitem__(self, key, value):
        """ Cannot set pixel item. """
        pass
    def __delitem__(self, key):
        """ Cannot delete pixel color. """
        pass
