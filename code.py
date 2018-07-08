import board
import digitalio
import time
import busio
import adafruit_pcf8523

adr=[]
## initialize i2c I/O of RTC
i2c = busio.I2C(board.SCL, board.SDA,frequency=400000)
rtc = adafruit_pcf8523.PCF8523(i2c)
if 'i2c' in locals() and 'rtc' in locals():
    t = rtc.datetime
    #print(t)
else:
    print("i2c bus and RTC not initialized !")
    quit()

print(t)
print(t.tm_year)
print(t.tm_mon)
print(t.tm_mday)
print(t.tm_hour)
print(t.tm_min)
print(t.tm_sec)
print(t.tm_wday)



#Led for output_signal
#led = digitalio.DigitalInOut(board.D13)
#led.direction = digitalio.Direction.OUTPUT

