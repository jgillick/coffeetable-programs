from .BaseShape import BaseShape
from .Animatable import Animatable, LivingAnimation
from random import randint
from math import pi, fabs, sin

MIN_WIDTH = 5
MAX_BRIGHTNESS = 255

MIN_HORZ_SPEED = 5000
MAX_HORZ_SPEED = 15000

MIN_WIDTH_SPEED = 5000
MAX_WIDTH_SPEED = 15000

MIN_VERT_SPEED = 3000
MAX_VERT_SPEED = 30000

class Curve(BaseShape):
    """A basic sinewave curve."""
    animatable_attrs = ["width", "horizontal", "amplitude"]

    # The increment of PI per LED for the curve
    pi_inc = 0

    # Width animation
    width = None

    # Horizontam movement animation (indexed by the center of the curve)
    horizontal = None

    # Veritical animation
    amplitude = None

    # The first LED in the curve
    first_led = 0

    # The last LED in the curve
    last_led = 0

    # The starting x value to generate the sine wave from
    start_x = 0

    def __init__(self, led_count, color, time):
        super().__init__(led_count, color, time)
        self.create_curve()


    def create_curve(self):
        """Create a new curve to animate to."""
        self._define_amplitude()
        self._define_width()
        self._define_horizontal()
        self._cache_values()
        print("New Curve")
        print(self)


    def update(self, now):
        is_animating = super().update(now)

        # Animation complete, generate new curve
        if not is_animating:
            self.create_curve()
        else:
            self._cache_values()


    def _define_amplitude(self):
        """ Define a random amplitude animation for the curve."""
        self.amplitude = LivingAnimation(
            label="Amplitude",
            initial_value=0,
            value_range={'min': 0, 'max': MAX_BRIGHTNESS},
            duration_range={'min': MIN_VERT_SPEED, 'max': MAX_VERT_SPEED}
        )

    def _define_width(self):
        """Define a random width for the curve."""
        if self.led_count < 5:
            min_width = 1
            max_width = self.led_count
        else:
            min_width = 5
            max_width = round(self.led_count / 2)
        self.width = LivingAnimation(
            label="Width",
            initial_value=randint(min_width, max_width),
            value_range={'min': min_width, 'max': max_width},
            duration_range={'min': MIN_WIDTH_SPEED, 'max': MAX_WIDTH_SPEED}
        )

    def _define_horizontal(self):
        """Define a random horizontal movement for the curve, defined as the center pixel.
        Using the center pixel means that the curve will always be at least half in the LED strip
        by choosing a random number between zero and the LED count.
        """
        self.horizontal = LivingAnimation(
            label="Horizontal",
            initial_value=randint(0, self.led_count),
            relative_range={'min': 0, 'max': self.led_count / 4},
            value_range={'min': 0, 'max': self.led_count},
            duration_range={'min': MIN_HORZ_SPEED, 'max': MAX_HORZ_SPEED}
        )


    def _cache_values(self):
        """Calculate values that will be used to generate LED colors later."""
        width = self.width.current
        self.pi_inc = pi / width

        # Add extra LED to both sides and adjust for fractional LED indexes
        width += 2
        center = self.horizontal.current + 1
        start = center - (width / 2)
        start_led = round(start)
        self.first_led = start_led
        self.last_led = self.first_led + width

        # If the starting LED was rounded, adjust the starting x value used for Math.sin accordintly
        # This makes a smoother transition to fade between LEDs as the curve moves.
        # For example, if start_led was .6, it will be rounded to 1. In that case, we'd want the previous LED to be
        # 40% of the first value (pi_inc * 1 - 0.6)
        if start != start_led:
            self.start_x = self.pi_inc * fabs(start - start_led)
        else:
            self.start_x = 0


    def __getitem__(self, idx):
        """Get an LED RGB tuple by index."""

        # Index out of range
        if (
            idx < 0
            or idx >= self.led_count
            or idx < self.first_led
            or idx > self.last_led
            or self.first_led == self.last_led
        ):
            return (0, 0, 0)

        colors = [0, 0, 0]

        # Generate brightness from math.sin
        curve_idx = idx - self.first_led
        curve_x = self.start_x + (self.pi_inc * curve_idx)
        amplitude = self.amplitude.current
        brightness = round(amplitude * sin(curve_x))

        # Adjust for min/max values
        if brightness < 0:
            brightness = 0
        elif brightness > 255:
            brightness = 255

        # Assign to color
        colors[self.color] = brightness
        return tuple(colors)


    def __repr__(self):
        out = f"Curve: (pi_inc={self.pi_inc}, first_led={self.first_led}, last_led={self.last_led})"
        for anin_attr in self.animatable_attrs:
            anim = getattr(self, anin_attr)
            out += f"\n  {anin_attr}= {{{anim}}}"
        return out
