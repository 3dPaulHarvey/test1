import asyncio
import math
import time
import moteus
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Extended Limit Switch
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Home Limit Switch
GPIO.output(16,GPIO.LOW)  #Indicator LED

c = moteus.Controller()

##############Start Up

async def start_up():
#Zero
    await c.set_stop()
    await c.set_rezero(rezero=0.0, query=False)
    c_data = await c.query()
    initial_position = c_data.values[moteus.Register.POSITION]
    await asyncio.sleep(0.1)

# Hold Start Position
    for x in range(50):
        await c.set_position(position=initial_position, velocity=0.0, watchdog_timeout=math.nan, query=False)
        await asyncio.sleep(0.01)

# Homing Sequence
    c_data = await c.query()
    c_torque = c_data.values[3]
    initial_position = c_data.values[1]
    print ("torque")
    print(c_torque)
    while c_torque < .5:
        c_data = await c.query()
        c_torque = c_data.values[3]
        await c.set_position(position=initial_position, velocity=4.0,  kp_scale=0.8, maximum_torque=None, query=True)
        initial_position += 0.02
        await asyncio.sleep(0.02)
    print(await c.query())

# Hold Homed
    c_data = await c.query()
    current_position = c_data.values[moteus.Register.POSITION]
    for y in range(50):
        await c.set_position(position=current_position, velocity=0.0, watchdog_timeout=math.nan, query=False, kp_scale=10)
        await asyncio.sleep(0.001)
# Movement to New Home
    c_data = await c.query()
    current_position = c_data.values[moteus.Register.POSITION]
    new_home = current_position - 0.25
    while current_position > new_home:
        current_position -= 0.001
        await c.set_position(position=current_position, velocity=2.0, query=False)

# Hold New Home
    GPIO.output(16,GPIO.HIGH)
    c_data = await c.query()
    new_home_done = c_data.values[moteus.Register.POSITION]
    for y in range(50):
        await c.set_position(position=new_home_done, velocity=0.0, kp_scale=5, maximum_torque=0.5, watchdog_timeout=math.nan,  query=False)
        await asyncio.sleep(0.001)
    print("homed at ")
    print(new_home_done)

#####################Extend 

async def extend():
    c_data = await c.query()
    position_10 = c_data.values[moteus.Register.POSITION]
    desired_pos = position_10 -1.72   #5
    kp=None
    feedforward=None
    max_torque = 0.0

    while True:
        result = await c.set_position(
            position=math.nan,
            stop_position=desired_pos,
            velocity=15.0,
            maximum_torque=None,
            velocity_limit=30.0,
            #accel_limit=315.0,
            watchdog_timeout=math.nan,
            feedforward_torque=feedforward,
            kp_scale=1.3,
            kd_scale=1,
            query=True)
        
        # if result is None:
        #     print("none")
        #     continue
        # if (result.values[moteus.Register.TORQUE] > max_torque):
        #     max_torque = result.values[moteus.Register.TORQUE]
        # if max_torque > 2:
        #     break
        error_cm = (result.values[moteus.Register.POSITION] -
                    desired_pos)
        if (abs(error_cm) < 0.05):
            break
    
    c_data = await c.query()
    print(c_data)

    await asyncio.sleep(0.1)
    await c.set_stop()
    await asyncio.sleep(0.1)
    await c.set_position(position=math.nan, velocity=0.0,  kp_scale=10,  maximum_torque=None, watchdog_timeout=math.nan)
    print("stopped 6")

    c_data = await c.query()
    print(c_data)
    print("max torque")
    print(max_torque)

###################Sheath Function
async def sheath():
    c_data = await c.query()
    position_10 = c_data.values[moteus.Register.POSITION]
    desired_pos = position_10 + 1.675 #4   
    kp=None
    feedforward=None
    max_torque = 0.0

    while True:
        result = await c.set_position(
            position=math.nan,
            stop_position=desired_pos,
            velocity=18.0,
            maximum_torque=None,
            #velocity_limit=30.0,
            #accel_limit=315.0,
            watchdog_timeout=math.nan,
            feedforward_torque=feedforward,
            kp_scale=1.3,
            kd_scale=1,
            query=True)
        
        # if result is None:
        #     print("none")
        #     continue
        # if (result.values[moteus.Register.TORQUE] > max_torque):
        #     max_torque = result.values[moteus.Register.TORQUE]
        # if max_torque > 2:
        #     break
        error_cm = (result.values[moteus.Register.POSITION] -
                    desired_pos)
        if (abs(error_cm) < 0.05):
            break
    
    c_data = await c.query()
    print(c_data)

    await asyncio.sleep(0.1)
    await c.set_stop()
    await asyncio.sleep(0.1)
    await c.set_position(position=math.nan, velocity=0.0,  kp_scale=10,  maximum_torque=None, watchdog_timeout=math.nan)
    print("sheathed1")

    c_data = await c.query()
    print(c_data)
    print("max torque")
    print(max_torque)

# Re-Homing Sequence
# Homing Sequence
    c_data = await c.query()
    c_torque = c_data.values[3]
    initial_position = c_data.values[1]
    while c_torque < .5:
        c_data = await c.query()
        c_torque = c_data.values[3]
        await c.set_position(position=initial_position, velocity=2,  kp_scale=0.8, maximum_torque=None, query=True)
        initial_position += 0.02
        await asyncio.sleep(0.02)
    print(await c.query())

# Movement to New Home 2
    c_data = await c.query()
    current_position = c_data.values[moteus.Register.POSITION]
    new_home = current_position - 0.25
    while current_position > new_home:
        current_position -= 0.001
        await c.set_position(position=current_position, velocity=2.0, query=False)

# Hold New Home 2
    GPIO.output(16,GPIO.HIGH)
    c_data = await c.query()
    done_position_4 = c_data.values[moteus.Register.POSITION]
    for y in range(50):
        c_data = await c.set_position(position=done_position_4, velocity=0.0, kp_scale=7.0, maximum_torque=None, watchdog_timeout=math.nan, query=True)
        await asyncio.sleep(0.001)
        c_torque = c_data.values[3]
        print (c_torque)



#######ShutDown
async def shutdown():
    print(await c.query())
    await c.set_stop()



##############Main
async def main():

    await start_up()

    while (1):
        c_data = await c.query()
        print(c_data.values[moteus.Register.TORQUE])
        x3 = input("press to extend")
        await extend()
        
        x2 = input("press to sheath")
        c_data = await c.query()
        print(c_data.values[moteus.Register.TORQUE])
        await sheath()


######Program Start
if __name__ == '__main__':
    asyncio.run(main())