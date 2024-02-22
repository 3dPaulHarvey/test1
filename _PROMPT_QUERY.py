#This is how to use the Moteus Controller query functionality
#this allows you to check the status of the Moteus bldc controller and bldc
import asyncio
import moteus

async def main():
    # Create an instance of the Moteus controller for a specific ID.
    # In this example, we are using controller with ID=1.
    c = moteus.Controller(id=1)
    
    # Query the controller to get its current status.
    # This sends a request to the controller and awaits its response.
    c_data = await c.query()
    
    # Accessing individual attributes from the response.
    # These attributes are derived from the dictionary stored in `c_data.values`.
    # If an attribute does not exist in the dictionary, the `get` method returns None.

    # Get the operating mode of the controller (e.g., position control, velocity control).
    mode = c_data.values.get(0x000)
    
    # Get the current position of the motor (typically in units of revolutions or radians).
    position = c_data.values.get(0x001)
    
    # Get the current velocity of the motor (e.g., revolutions per second).
    velocity = c_data.values.get(0x002)
    
    # Get the current torque output of the motor.
    torque = c_data.values.get(0x003)
    
    # Get the voltage being applied to the motor.
    voltage = c_data.values.get(0x00d)
    
    # Get the current temperature of the motor (typically in degrees Celsius).
    temperature = c_data.values.get(0x00e)
    
    # Get any fault codes or status. This can indicate issues such as over-temperature or electrical faults.
    fault = c_data.values.get(0x00f)
    
    # Print the retrieved attributes to the console.
    print(f"Mode: {mode}")
    print(f"Position: {position}")
    print(f"Velocity: {velocity}")
    print(f"Torque: {torque}")
    print(f"Voltage: {voltage}")
    print(f"Temperature: {temperature}")
    print(f"Fault: {fault}")

# Start the asynchronous event loop and run our main function.
# This initiates the process of querying the controller and printing the results.
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
