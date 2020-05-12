import board
import time
import adafruit_dotstar as dotstar

from shapes.BaseShape import RED, BLUE, GREEN
from shapes.Curve import Curve

# LED_PINS = board.PA7
LED_NUM = 144
LED_PIN_DATA = board.MOSI
LED_PIN_CLK = board.SCK
# LED_PROTOCOL_ORDER = neopixel.GRB

MIN_BRIGHTNESS = 0

# pixels = neopixel.NeoPixel(LED_PINS, LED_NUM, brightness=0.2, auto_write=False,
#                            pixel_order=LED_PROTOCOL_ORDER)
pixels = dotstar.DotStar(board.SCK, board.MOSI, LED_NUM, auto_write=False, brightness=0.5, baudrate=1000000)


def millis():
    """Return the number of milliseconds which have elapsed since the CPU turned on."""
    return time.monotonic() * 1000

def main():
    curves = [
        # Curve(LED_NUM, RED, millis()),
        Curve(LED_NUM, GREEN, millis()),
        # Curve(LED_NUM, BLUE, millis()),
    ]

    while True:
        pixels.fill((MIN_BRIGHTNESS, MIN_BRIGHTNESS, MIN_BRIGHTNESS))

        # Update curve animation
        for curve in curves:
            curve.update(millis())

        # Set LED colors
        for i in range(LED_NUM):
            (r, g, b) = (MIN_BRIGHTNESS, MIN_BRIGHTNESS, MIN_BRIGHTNESS)

            # Take the maximum pixel value for all curves
            for curve in curves:
                (cr, cg, cb) = curve[i]
                r = max(r, cr)
                g = max(r, cg)
                b = max(r, cb)

            pixels[i] = (r,g,b)
        pixels.show()

        # print("---------------------")
        # print(pixels)

        # Sleep for 1ms
        time.sleep(0.5)
