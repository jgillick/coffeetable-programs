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
pixels = dotstar.DotStar(board.SCK, board.MOSI, LED_NUM, auto_write=False, brightness=1)

# Gamma correction table
gamma = [
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255
]

def millis():
    """Return the number of milliseconds which have elapsed since the CPU turned on."""
    return time.monotonic() * 1000

def main():
    curves = [
        Curve(LED_NUM, RED, millis()),
        Curve(LED_NUM, GREEN, millis()),
        Curve(LED_NUM, BLUE, millis()),
        Curve(LED_NUM, GREEN, millis()),
    ]

    while True:
        now = millis()

        # Update curve animation
        for curve in curves:
            curve.update(now)

        # Set LED colors
        for i in range(LED_NUM):
            (r, g, b) = (MIN_BRIGHTNESS, MIN_BRIGHTNESS, MIN_BRIGHTNESS)

            # Take the maximum pixel value for all curves
            for curve in curves:
                (cr, cg, cb) = curve[i]
                r = max(r, cr)
                g = max(g, cg)
                b = max(b, cb)

            # Set color with gamma correction
            pixels[i] = (
                gamma[r],
                gamma[g],
                gamma[b],
            )

        pixels.show()
        time.sleep(0.001)

main()