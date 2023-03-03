# NOTE: Run this program with the latest
# firmware provided via https://beta.pybricks.com/

from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from pybricks.tools import wait

# Standard MicroPython modules
from usys import stdout



stdout.buffer.write(bytearray("Start,"))
stdout.buffer.write(bytearray(
    "Duty cycle [%],"
    "Hub battery voltage [mV],"
    "Hub battery supplied current [mA],"
    "Motor speed [deg/s]," 
    "Motor load [mNm],"  
    "Time [ms]"             
))
stdout.buffer.write(bytearray("Header-To-Data;"))

for i in range(500): #From 5 to 6 makes it stall on the reciever end.
    string = f"0.1111,0.1111,0.1111,0.1111,0.1111,0.1111;"
    stdout.buffer.write(bytearray(string))
stdout.buffer.write(bytearray("Done"))


