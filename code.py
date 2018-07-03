import board
import digitalio
import time
import busio
import adafruit_pcf8523

#Scan for I2C device 
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


#Led for output_signal
#led = digitalio.DigitalInOut(board.D13)
#led.direction = digitalio.Direction.OUTPUT

##initialize variables
#t = rtc.datetime
#print(t)
#print(t.tm_date,t.tm_hour, t.tm_min)
