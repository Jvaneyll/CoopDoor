import board
import digitalio
import time
import busio
import adafruit_pcf8523

## initialize i2c I/O of RTC
i2c = busio.I2C(board.SCL, board.SDA,frequency=400000)
rtc = adafruit_pcf8523.PCF8523(i2c)
if 'i2c' in locals() and 'rtc' in locals():
    now = rtc.datetime
    #print(now)
else:
    print("i2c bus and RTC not initialized !")
    quit()

print(now)
print(now.tm_year)
print(now.tm_mon)
print(now.tm_mday)
print(now.tm_hour)
print(now.tm_min)
print(now.tm_sec)
print(now.tm_wday)



#Led for output_signal
#led = digitalio.DigitalInOut(board.D13)
#led.direction = digitalio.Direction.OUTPUT

