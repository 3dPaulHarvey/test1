from gpiozero import Button, RGBLED
from signal import pause

# Initialize RGB LED connected to pins 12, 13, and 19
led = RGBLED(red=12, green=13, blue=19)

# Initialize buttons connected to pins 5 and 6
button1 = Button(5)  # Represents the Extended button
button2 = Button(6)  # Represents the Homed button
button3 = Button(4)  # Represents the Activate button
button4 = Button(3)  # Represents the Safety button

# Define functions to run when buttons are pressed
def on_button1_pressed():
    led.color = (0, 0, 1)  # Blue (Extended)

def on_button2_pressed():
    led.color = (0, 1, 0)  # Green (Homed)

def on_button3_pressed():
    led.color = (1, 0, 0) 

def on_button4_pressed():
    led.color = (.5, 0, .5)  

# Attach functions to button press events
button1.when_pressed = on_button1_pressed  # Extended button
button2.when_pressed = on_button2_pressed  # Homed button
button3.when_pressed = on_button3_pressed  
button4.when_pressed = on_button4_pressed  

pause()  # Keep the program running
