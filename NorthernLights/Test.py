import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
import numpy as np
from time import sleep

from shapes.Curve import Curve
from shapes.BaseShape import RED, BLUE, GREEN

LED_NUM = 150
COLORS = ['red', 'green', 'blue']
SPEED = 100

curves = []
milliseconds = 0
running = False
run_next = False
pause_btn = None
next_btn = None

def millis():
    global milliseconds
    return milliseconds

def toggle_pause(event):
    global running
    global pause_btn, next_btn
    running = not running
    if running:
        pause_btn.label.set_text('Pause')
    else:
        pause_btn.label.set_text('Play')
    next_btn.set_active(not running)

def next_step(event):
    global run_next
    run_next = True

def loop(i, ax, xs):
    global milliseconds, running, run_next

    if not running and not run_next:
        return
    run_next = False

    milliseconds += SPEED

    ax.clear()
    setup_chart(ax)

    # Update curve animation
    i = 0
    for curve in curves:
        curve.update(milliseconds)
        ys = [curve[i][curve.color] for i in range(LED_NUM)]

        # Update coordinates
        ax.plot(xs, ys, color=COLORS[curve.color])
        i += 1

def setup_chart(ax):
    ax.set_xlim([0, LED_NUM-1])
    ax.set_ylim([0, 255])
    ax.set_autoscaley_on(False)

def main():
    global pause_btn, next_btn

    # Create curves
    curves.append(Curve(LED_NUM, RED, milliseconds))
    sleep(.5)
    curves.append(Curve(LED_NUM, GREEN, milliseconds))
    sleep(.1)
    curves.append(Curve(LED_NUM, BLUE, milliseconds))

    # Setup plots
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)
    setup_chart(ax)

    # X values
    xs = list(range(LED_NUM))

    # Add buttons
    axpause = plt.axes([0.7, 0.05, 0.1, 0.075])
    axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
    pause_btn = Button(axpause, 'Play')
    pause_btn.on_clicked(toggle_pause)
    next_btn = Button(axnext, 'Next')
    next_btn.set_active(True)
    next_btn.on_clicked(next_step)

    # Start animation
    ani = animation.FuncAnimation(fig, loop, fargs=(ax, xs), interval=SPEED)
    plt.show()

main()