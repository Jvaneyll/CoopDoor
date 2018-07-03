##DESCRIPTION
# The objective of this script is to control a DC motor (via H bridge logic) at every sunrise and sunset using the Trinket M0 controller board and an I2C-connected Real Time Controller (RTC) module.
# The RTC module is PCF8523 and has been initialized on a Rpi3B upfront.

##INIT VARIABLES AND LIBRARIES
import board
import digitalio
import time
import busio
import adafruit_pcf8523

##INIT I2C connection

i2c = busio.I2C(board.SCL, board.SDA)
 
while not i2c.try_lock():
    pass
 
 
while True:
    adr= i2c.scan()
    print("I2C addresses found:", [hex(device_address)
                                   for device_address in i2c.scan()])
    #if adr
    #    rtc = adafruit_pcf8523.PCF8523(i2c)
    time.sleep(0.1)

## initialize I/O

#I2C for RTC clock
#i2c_bus = busio.I2C(board.SCL, board.SDA)
#print(i2c_bus)

##initialize variables
#t = rtc.datetime
#print(t)
#print(t.tm_date,t.tm_hour, t.tm_min)

##FUNCTIONS DEFINITIONS

#Calculate next sunrise

#Calculate next sunset

#Open door

#Close door

##INIT BOARD AND STATUS

##RUN PROGRAM
