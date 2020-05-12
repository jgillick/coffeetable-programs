import time
import board
import neopixel
import random
import math

LED_PINS = board.PA7
LED_NUM = 65
LED_PROTOCOL_ORDER = neopixel.GRB

MIN_BRIGHTNESS = 10
MAX_BRIGHTNESS = 255
MIN_WIDTH = 5
MAX_WIDTH = LED_NUM

MIN_HORZ_SPEED = 5000
MAX_HORZ_SPEED = 15000
MIN_VERT_SPEED = 3000
MAX_VERT_SPEED = 30000

pixels = neopixel.NeoPixel(LED_PINS, LED_NUM, brightness=0.2, auto_write=False,
                           pixel_order=LED_PROTOCOL_ORDER)

curves = []

def millis():
  return time.monotonic() * 1000

def setupAnimation(curve):
    animation = curve['animation']
    vert = curve['vert']
    horz = curve['horz']
    width = curve['width']

    # Vertical
    vertTime = random.randint(MIN_VERT_SPEED, MAX_VERT_SPEED)
    vert['time'] = vertTime
    vert['incPerMs'] = (vert['target'] - vert['current']) / vertTime

    #   Horizontal movement
    half = round(width['target'] / 2)
    moveTo = random.randint(half * -1, MAX_WIDTH - half)
    horzTime = random.randint(MIN_HORZ_SPEED, MAX_HORZ_SPEED)
    horz['target'] = moveTo
    horz['time'] = horzTime
    horz['incPerMs'] = (moveTo - horz['current']) / horzTime

    # Width
    width['time'] = 0
    width['msInc'] = 0
    widthTime = 0
    if width['current'] != width['target']:
        width['time'] = random.randint(MIN_HORZ_SPEED, MAX_HORZ_SPEED)
        width['incPerMs'] = (width['target'] - width['current']) / width['time']

    animTime = max(vertTime, horzTime, widthTime)
    animation['start'] = millis()
    animation['done'] = animation['start'] + animTime
    animation['lastMove'] = animation['start']


def createCurve(fromCurve=None, color=0):
    amplitude = random.randint(0, MAX_BRIGHTNESS - MIN_BRIGHTNESS)
    width = random.randint(MIN_WIDTH, MAX_WIDTH)
    piInc = math.pi / width

    if fromCurve:
        offset = fromCurve['horz']['current']
    else:
        center = random.randint(0, LED_NUM)
        offset = int(center - (width/2))

    curveConfig = {
        'piInc': piInc,
        'lastTime': millis(),
        'color': color if fromCurve is None else fromCurve['color'],
        'animation': {
            'start': 0,
            'done': 0,
            'lastMove': 0,
        },
        'horz': {
            'incPerMs': 0,
            'target': offset,
            'current': offset if fromCurve is None else fromCurve['horz']['current'],
        },
        'vert': {
            'target': amplitude,
            'current': 0 if fromCurve is None else fromCurve['vert']['current'],
        },
        'width': {
            'incPerMs': 0,
            'target': width,
            'current': width if fromCurve is None else fromCurve['width']['current'],
        }
    }

    setupAnimation(curveConfig)
    return curveConfig


def animationConfigUpdate(elapsedMs, conf):
    if conf['current'] == conf['target']:
      return

    incPerMs = conf['incPerMs']
    current = conf['current']
    target = conf['target']
    conf['current'] += conf['incPerMs'] * elapsedMs

    # Animation complete
    if (
        (incPerMs > 0 and current >= target)
        or (incPerMs < 0 and current <= target)
    ):
        conf['incPerMs'] = 0
        conf['current'] = conf['target']


def moveCurve(curve):
    now = millis()
    animation = curve['animation']
    vert = curve['vert']
    horz = curve['horz']
    width = curve['width']
    elapsedMs = now - animation['lastMove']
    animation['lastMove'] = now

    # Vertical move
    if vert['incPerMs']:
        animationConfigUpdate(elapsedMs, vert)

    # Horizontal move
    if horz['incPerMs']:
        animationConfigUpdate(elapsedMs, horz)

    # Width adjust
    if width['incPerMs']:
        animationConfigUpdate(elapsedMs, width)

    # We've completed the animation, generate new curve
    if now >= animation['done']:
        print("New curve (%d)" % curve['color'])
        return createCurve(curve)
    return curve


def updateLEDs():
    #leds = [MIN_BRIGHTNESS] * LED_NUM
    pixels.fill((MIN_BRIGHTNESS, MIN_BRIGHTNESS, MIN_BRIGHTNESS))

    # Set LED colors
    for curve in curves:
        horz = curve['horz']
        vert = curve['vert']
        width = curve['width']
        offset = round(horz['current'])
        horzShift = horz['current'] - offset
        width = width['current']
        colorIdx = curve['color']

        offset -= 1
        width += 2

        piInc = math.pi / width
        piTick = 0
        if horzShift != 0:
            piTick = piInc * math.fabs(horzShift)

        for i in range(width):
            ledIdx = i + offset
            if ledIdx < 0 or ledIdx >= LED_NUM:
                continue

            brightness = (vert['current'] * math.sin(piTick)) + MIN_BRIGHTNESS
            if brightness < MIN_BRIGHTNESS:
                brightness = MIN_BRIGHTNESS
            elif brightness >= MAX_BRIGHTNESS:
                brightness = MAX_BRIGHTNESS

            useColor = round(max(pixels[ledIdx][colorIdx], brightness))

            r, g, b = pixels[ledIdx]
            if colorIdx == 0:
                r = useColor
            elif colorIdx == 1:
                g = useColor
            elif colorIdx == 2:
                b = useColor
            pixels[ledIdx] = (r,g,b)
            piTick += piInc

    pixels.show()


curves = [
    #createCurve(None, 0),
    createCurve(None, 1),
    createCurve(None, 2),
]
while True:
    updateLEDs()
    for i in range(len(curves)):
        curves[i] = moveCurve(curves[i])
    time.sleep(.001)