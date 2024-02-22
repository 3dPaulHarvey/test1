from gpiozero import RGBLED, Button
from signal import pause
import asyncio
import math
import moteus

c = moteus.Controller()

led = RGBLED(red=12, green=13, blue=19)

extended_button = Button(5)
home_button = Button(6)

BLUE = (0, 0, 1)
GREEN = (0, 1, 0)
RED = (1, 0, 0)

def update_led_color():
    if home_button.is_pressed:
        led.color = GREEN
    elif extended_button.is_pressed:
        led.color = BLUE
    else:
        led.color = RED

extended_button.when_pressed = update_led_color
home_button.when_pressed = update_led_color

async def startup_led_control():
    while True:
        update_led_color()
        await asyncio.sleep(0.1)

async def homing():
    led_task = asyncio.create_task(startup_led_control())

    #Zeros the motors position
    await c.set_stop()
    await c.set_rezero(rezero=0.0, query=False)
    c_data = await c.query()
    initial_position = c_data.values[moteus.Register.POSITION]
    await asyncio.sleep(0.1)

    #Move towards home
    while not home_button.is_pressed:
        c_data = await c.set_position(position=math.nan, velocity=1.0, kp_scale=0.8, maximum_torque=None, watchdog_timeout=math.nan, query=True)
 
    led.color = GREEN  # Indicate successful homing
    
    #Hold Home Position 
    c_data = await c.query()
    home_position = c_data.values[moteus.Register.POSITION]
    await c.set_position(position=home_position, velocity=0.0, kp_scale=10, maximum_torque=None, watchdog_timeout=math.nan)

    #check torque
    c_data = await c.query()
    for x in range(0, 100):
        c_torque = c_data.values[3]        
        print (c_torque)
        await asyncio.sleep(0.02)

async def extend():
    c_data = await c.query()
    position_10 = c_data.values[moteus.Register.POSITION]
    desired_pos = position_10 - 1.72
    kp = None
    feedforward = None
    max_torque = 0.0

    while True:
        result = await c.set_position(
            position=math.nan,
            stop_position=desired_pos,
            velocity=15.0,
            maximum_torque=None,
            velocity_limit=30.0,
            watchdog_timeout=math.nan,
            feedforward_torque=feedforward,
            kp_scale=1.3,
            kd_scale=1,
            query=True)

        error_cm = (result.values[moteus.Register.POSITION] - desired_pos)
        if abs(error_cm) < 0.05:
            break

    c_data = await c.query()
    await asyncio.sleep(0.1)
    await c.set_stop()
    await asyncio.sleep(0.1)
    await c.set_position(position=math.nan, velocity=0.0, kp_scale=10, maximum_torque=None, watchdog_timeout=math.nan)

async def sheath():
    c_data = await c.query()
    position_10 = c_data.values[moteus.Register.POSITION]
    desired_pos = position_10 + 1.675
    kp = None
    feedforward = None
    max_torque = 0.0

    while True:
        result = await c.set_position(
            position=math.nan,
            stop_position=desired_pos,
            velocity=18.0,
            maximum_torque=None,
            watchdog_timeout=math.nan,
            feedforward_torque=feedforward,
            kp_scale=1.3,
            kd_scale=1,
            query=True)

        error_cm = (result.values[moteus.Register.POSITION] - desired_pos)
        if abs(error_cm) < 0.05:
            break

    c_data = await c.query()
    await asyncio.sleep(0.1)
    await c.set_stop()
    await asyncio.sleep(0.1)
    await c.set_position(position=math.nan, velocity=0.0, kp_scale=10, maximum_torque=None, watchdog_timeout=math.nan)

async def shutdown():
    await c.set_stop()

async def main():
    await homing()

    while True:
        c_data = await c.query()

        x3 = input("Press Enter to extend")
        await extend()

        x2 = input("Press Enter to sheath")
        c_data = await c.query()
        await sheath()

if __name__ == '__main__':
    asyncio.run(main())
    pause()
