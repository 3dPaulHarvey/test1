import asyncio
import math
import time
import moteus


async def thing():

    print(1)
    c = moteus.Controller()  # initialize Controller
    print(2)
    c_data = await c.query()  # collect controller data
    print(3)

    # CLEAR CONTROLLER FOR MOVEMENT
    print("CLEAR FOR MOVEMENT")
    await c.set_stop()  # stop controller to wait for next command - (maybe us watchdog timeout)


asyncio.run(thing())
