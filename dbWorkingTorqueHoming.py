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

def update_led_color():
    if home_button.is_pressed:
        led.color = GREEN
    elif extended_button.is_pressed:
        led.color = BLUE
    else:
        led.color = (0, 0, 0)

extended_button.when_pressed = update_led_color
home_button.when_pressed = update_led_color

async def startup_led_control():
    while True:
        update_led_color()
        await asyncio.sleep(0.1)

async def start_up():
    led_task = asyncio.create_task(startup_led_control())

    await c.set_stop()
    await c.set_rezero(rezero=0.0, query=False)
    c_data = await c.query()
    initial_position = c_data.values[moteus.Register.POSITION]
    await asyncio.sleep(0.1)

    for x in range(50):
        await c.set_position(position=initial_position, velocity=0.0, watchdog_timeout=math.nan, query=False)
        await asyncio.sleep(0.01)

    c_data = await c.query()
    c_torque = c_data.values[3]
    initial_position = c_data.values[1]

    while c_torque < 0.5:
        c_data = await c.query()
        c_torque = c_data.values[3]
        await c.set_position(position=math.nan, velocity=1.0, kp_scale=0.8, maximum_torque=None, query=True)
        #initial_position += 0.02
        await asyncio.sleep(0.02)

    c_data = await c.query()
    current_position = c_data.values[moteus.Register.POSITION]

    for y in range(50):
        await c.set_position(position=current_position, velocity=0.0, watchdog_timeout=math.nan, query=False, kp_scale=10)
        await asyncio.sleep(0.001)

    c_data = await c.query()
    current_position = c_data.values[moteus.Register.POSITION]
    new_home = current_position - 0.25

    while current_position > new_home:
        current_position -= 0.001
        await c.set_position(position=current_position, velocity=2.0, query=False)

    c_data = await c.query()
    new_home_done = c_data.values[moteus.Register.POSITION]

    for y in range(50):
        await c.set_position(position=new_home_done, velocity=0.0, kp_scale=5, maximum_torque=0.5, watchdog_timeout=math.nan, query=False)
        await asyncio.sleep(0.001)

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

    #clear fault if we went to fast or over voltage
    c_data = await c.query()
    await asyncio.sleep(0.1)
    await c.set_stop()
    await asyncio.sleep(0.1)
    await c.set_position(position=math.nan, velocity=0.0, kp_scale=10, maximum_torque=None, watchdog_timeout=math.nan)

   # c_data = await c.query()
   # new_home_done = c_data.values[moteus.Register.POSITION]

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

    c_data = await c.query()
    c_torque = c_data.values[3]
    initial_position = c_data.values[1]

    while c_torque < 0.5:
        c_data = await c.query()
        c_torque = c_data.values[3]
        await c.set_position(position=initial_position, velocity=2, kp_scale=0.8, maximum_torque=None, query=True)
        initial_position += 0.02
        await asyncio.sleep(0.02)

    c_data = await c.query()
    current_position = c_data.values[moteus.Register.POSITION]
    new_home = current_position - 0.25

    while current_position > new_home:
        current_position -= 0.001
        await c.set_position(position=current_position, velocity=2.0, query=False)


    c_data = await c.query()
    done_position_4 = c_data.values[moteus.Register.POSITION]

    for y in range(50):
        c_data = await c.set_position(position=done_position_4, velocity=0.0, kp_scale=7.0, maximum_torque=None, watchdog_timeout=math.nan, query=True)
        await asyncio.sleep(0.001)
        c_torque = c_data.values[3]

async def shutdown():
    await c.set_stop()

async def main():
    await start_up()

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
