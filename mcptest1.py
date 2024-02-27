# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008




# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


# Main program loop.
while True:


    values = mcp.read_adc(0)
    
    print(values)
    mapped = map_value(values,0, 1023, 0.0, 10.0)
    print(mapped)
    time.sleep(0.1)