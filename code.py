import board
import digitalio
import busio
import adafruit_pcf8523
from datetime import date, timedelta, datetime, time, tzinfo
from math import sin, cos, pi, floor, asin, acos, sqrt
i2c = busio.I2C(board.SCL, board.SDA,frequency=400000)
rtc = adafruit_pcf8523.PCF8523(i2c)
if 'i2c' in locals() and 'rtc' in locals():
    now = rtc.datetime
    print(now)
else:
    print("i2c bus and RTC not initialized !")
    quit()
def sinrad(deg):
    return sin(deg * pi/180)
def cosrad(deg):
    return cos(deg * pi/180)
def calculatetimefromjuliandate(jd):
    jd=jd+.5
    secs=int((jd-int(jd))*24*60*60+.5)
    mins=int(secs/60)
    hour=int(mins/60)  
    return time(hour, mins % 60, secs % 60)
def calcsunriseandsunset(dt):
    a=floor((14-dt.month)/12)
    y = dt.year+4800-a
    m = dt.month+(12*a) -3
    julian_date=dt.day+floor((153*m+2)/5)+365*y+floor(y/4)-floor(y/100)+floor(y/400)-32045
    n= julian_date - 2451545.0 + (68.184 / 86400)
    jstar = n - (longitude/360)
    M=(357.5291+0.98560028*jstar) % 360
    c=(1.9148*sinrad(M))+(0.0200*sinrad(2*M))+(0.0003*sinrad(3*M))
    l=(M+102.9372+c+180) % 360
    jtransit = jstar + 2451545.0 + (0.0053 * sinrad(M)) - (0.0069 * sinrad(2 * l))
    delta=asin(sinrad(l) * sinrad(23.45))*180/pi
    H = acos((sinrad(-0.83+sqrt(150)/60*-2.076)-sinrad(latitude)*sinrad(delta))/(cosrad(latitude)*cosrad(delta)))*180/pi
    jset=jtransit + (H/360)
    jrise=jtransit - (H/360)
    return (calculatetimefromjuliandate(jrise), calculatetimefromjuliandate(jset))

longitude=4.677301 #West
latitude=50.645144 #North
print(longitude,latitude)
def main():
    #now=datetime(2018, 12, 24)
    sunrise,sunset = calcsunriseandsunset(now)
    print sunrise, sunset
if __name__ == '__main__':
    main()
