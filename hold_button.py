from gpiozero import Button, RGBLED
from signal import pause

# Initialize RGB LED connected to pins 12, 13, and 19
led = RGBLED(red=12, green=13, blue=19)

# Initialize the button connected to pin 5
button = Button(6)

# Define functions to change LED color on button events
def on_button_pressed():
    print("pressed")
    pass  # Do nothing on press

def on_button_released():
    led.color = (0, 0, 0)  # Turn off LED when button is released

def on_button_held():
    led.color = (1, 0, 0)  # Turn LED red when button is held

# Attach functions to button events
button.when_pressed = on_button_pressed
button.when_released = on_button_released
button.when_held = on_button_held


pause()  # Keep the program running
