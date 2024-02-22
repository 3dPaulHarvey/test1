import asyncio
import math
from gpiozero import RGBLED, Button

import moteus

c = moteus.Controller()
led = RGBLED(red=12, green=13, blue=19)
home_button = Button(6)
activate_button = Button(4)
extend_button = Button(5)

BLUE = (0, 0, 1)
GREEN = (0, 1, 0)
RED = (1, 0, 0)




async def homing():
    obstruction_encountered = False

    await c.set_stop()
    await c.set_rezero(rezero=0.0, query=False)
    await asyncio.sleep(0.1)

    while not home_button.is_pressed:
        c_data = await c.query()
        c_torque = c_data.values.get(moteus.Register.TORQUE, 0)

        if c_torque > 0.5:
            obstruction_encountered = True
            led.color = RED
            
            await c.set_position(position=math.nan, velocity=-0.5, kp_scale=1, maximum_torque=None, watchdog_timeout=math.nan)
            await asyncio.sleep(.25) 
            
            c_data = await c.query()
            current_position = c_data.values[moteus.Register.POSITION]
            await c.set_position(position=current_position, velocity=0.0, kp_scale=10, maximum_torque=None, watchdog_timeout=math.nan)
            return obstruction_encountered

        await c.set_position(position=math.nan, velocity=1.0, kp_scale=0.8, maximum_torque=None, watchdog_timeout=math.nan, query=True)
        await asyncio.sleep(0.02)

    led.color = GREEN


    c_data = await c.query()
    home_position = c_data.values[moteus.Register.POSITION]
    await c.set_position(position=home_position, velocity=0.0, kp_scale=10, maximum_torque=None, watchdog_timeout=math.nan)
    await asyncio.sleep(1)
    
    return obstruction_encountered


async def extend():
    c_data = await c.query()
    position_10 = c_data.values[moteus.Register.POSITION]
    desired_pos = position_10 - 1
    kp = None
    feedforward = None
    max_torque = 0.0

    while True:
        c_data = await c.query()
        if extend_button.is_pressed:
            led.color = BLUE  # Indicate that the limit switch for extending has been hit
            current_position = c_data.values[moteus.Register.POSITION]
            await c.set_position(position=current_position, velocity=0.0, kp_scale=10, maximum_torque=None, watchdog_timeout=math.nan)
            return

        result = await c.set_position(
            position=math.nan,
            stop_position=desired_pos,
            velocity=1.0,
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

        await asyncio.sleep(0.02)

    #clear fault if we went to fast or over voltage
    c_data = await c.query()
    await asyncio.sleep(0.1)
    await c.set_stop()
    await asyncio.sleep(0.1)
    await c.set_position(position=math.nan, velocity=0.0, kp_scale=10, maximum_torque=None, watchdog_timeout=math.nan)
    


async def main():
    obstruction_encountered = await homing()
 
    while True:
        if activate_button.is_pressed:
            if obstruction_encountered:
                obstruction_encountered = await homing()
            else:
                await extend()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


