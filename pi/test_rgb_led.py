import config

from time import sleep
from gpiozero import RGBLED

# RGB LED to reflect the state of the garage door
# RED - CLOSED | GREEN - OPEN | YELLOW - MOVEMENT (OPENING OR CLOSING)
led = RGBLED(red=config.PIN_LED_RED, green=config.PIN_LED_GREEN, blue=config.PIN_LED_BLUE, pwm=True)


def switch_led_color(state):
    """
        Responsible for switching color of RGB LED based of door status.
    """
    # print(state)
    if state == "moving":
        print("yellow")
        led.color = (1, 1, 0)
        # led.blink(0.5, 0.5, 0.2, 0.2, (1, 1, 0), (0.1, 0.1, 0), 5, True)  # blink yellow
    elif state == "open":
        print("green")
        led.color = (0, 1, 0)
        # led.blink(0.5, 0.5, 0.2, 0.2, (0, 1, 0), (0, 0.1, 0), 5, True)  # blink green
    elif state == "close":
        print("red")
        led.color = (1, 0, 0)
        # led.blink(0.5, 0.5, 0.2, 0.2, (1, 0, 0), (0.1, 0, 0), 5, True)  # blink red
    else:
        led.color = (0, 0, 0)  # off


if __name__ == '__main__':
    while True:
        switch_led_color("moving")
        sleep(3)
        switch_led_color("open")
        sleep(3)
        switch_led_color("moving")
        sleep(3)
        switch_led_color("close")
        sleep(3)
