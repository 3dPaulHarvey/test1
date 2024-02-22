from gpiozero import RGBLED
from time import sleep

# Initialize the RGB LED with GPIO pin numbers for red, green, and blue
led = RGBLED(red=12, green=13, blue=19)

# Turn on the red color (full intensity) and turn off green and blue
led.color = (1, 0, 0)
sleep(2)  # Keep it on for 2 seconds

# Turn on the green color (full intensity) and turn off red and blue
led.color = (0, 1, 0)
sleep(2)  # Keep it on for 2 seconds

# Turn on the blue color (full intensity) and turn off red and green
led.color = (0, 0, 1)
sleep(2)  # Keep it on for 2 seconds

# Turn off all colors (LED off )
led.off()

# Release the resources (optional)
led.close()
