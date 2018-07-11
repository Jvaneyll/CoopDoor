##DESCRIPTION
# The objective of this script is to control a DC motor (via H bridge logic) at every sunrise and sunset using the Trinket M0 controller board and an I2C-connected Real Time Controller (RTC) module.
# The RTC module is PCF8523 and has been initialized on a Rpi3B upfront.

##INIT LIBRARIES
import board
import digitalio
import busio
import adafruit_pcf8523
import time
from math import sin, cos, pi, floor, asin, acos, sqrt
print("SCRIPT START")
##INIT I2C CONNECTION ON RTC AND GET CURRENT DATE
i2c = busio.I2C(board.SCL, board.SDA,frequency=400000)
rtc = adafruit_pcf8523.PCF8523(i2c)
if 'i2c' in locals() and 'rtc' in locals():
    now = rtc.datetime
    #print(now)
else:
    print("i2c bus and RTC not initialized ! EXIT")
    quit()

##INIT VARIABLES
longitude=4.677301 #West
latitude=50.645144 #North
altitude=150 #meters above sea level
status=1 #(Door open by default at start)
print("variables definition : log=",longitude,"lat=",latitude,"alt=",altitude,"door status=",status)
    
##DEFINE FUNCTIONS
print("function def starting")
def sinrad(deg):
    return sin(deg * pi/180)
def cosrad(deg):
    return cos(deg * pi/180)
    
def calcjuliandate2000(dt):
    #Calculate julian date from UTC date at 00:00 UTC
    a=floor((14-dt.tm_mon)/12)
    y = dt.tm_year+4800-a
    m = dt.tm_mon+(12*a) -3
    julian_date=dt.tm_mday+floor((153*m+2)/5)+365*y+floor(y/4)-floor(y/100)+floor(y/400)-32045
    #Calculate current Julian day
    ##2451545.0 : n Julian days since 01/01/2000
    ##68.184 / 86400 fractional Julian day for leap seconds and terrestrial time
    n= julian_date - 2451545.0 + (68.184 / 86400)
    jdf= ((dt.tm_hour-12)/24) + (dt.tm_min/1440) + (dt.tm_sec/86400) #julian day fraction (hours, min, seconds in the day)
    ##-12  as julian day starts at noon UTC time. Fraction is 0 at 12:00
    return(n,jdf)

def sunriseandsunset(n,longitude,latitude,altitude):
    #Calculate solar noon at longitude
    jstar = n - (longitude/360)
    #Calculate solar mean anomaly
    M=(357.5291+0.98560028*jstar) % 360
    #Calculate equation of the center
    #1.9148 is the coefficient of the Equation of the Center for the planet the observer is on (in this case, Earth)
    c=(1.9148*sinrad(M))+(0.0200*sinrad(2*M))+(0.0003*sinrad(3*M))
    #Calculate ecliptic longitude
    #102.9372 is a value for the argument of perihelion.
    l=(M+102.9372+c+180) % 360
    #Calculate solar transit (julian date of solar noon (highest sun position in the day)) ##since 01/01/2000
    jtransit = jstar + (0.0053 * sinrad(M)) - (0.0069 * sinrad(2 * l)) ## + 2451545.0 to get real julian day
    #Calculate declination of sun in rad
    delta=asin(sinrad(l) * sinrad(23.45))*180/pi
    #Calculate Hour angle
    H = acos((sinrad(-0.83+sqrt(altitude)/60*-2.076)-sinrad(latitude)*sinrad(delta))/(cosrad(latitude)*cosrad(delta)))*180/pi
    #Calculate julian sunrise and sunset from 01/01/2000 by adding/substracting Hour angle from zenith position
    jset=jtransit + (H/360)+ 0.020833
    #0.020833 is 30 min in fraction of julian day to delay the door closure a bit
    jrise=jtransit - (H/360)
    return (jrise, jset)

print("function def completed")
##RUN PROGRAM
print("start of infinite loop")
while True:
    now = rtc.datetime
    #vtime=(2018,12,15,16,15,39,-1,-1,-1) #(tm_year=2018, tm_mon=7, tm_mday=10, tm_hour=18, tm_min=22, tm_sec=39, tm_wday=2, tm_yday=-1, tm_isdst=-1)
    #now= time.struct_time(vtime)
    n,dfrac=calcjuliandate2000(now)
    print("now=",now,"n=",n,"dfrac=",dfrac,"n+dfrac=",n+dfrac)
    today_sunrise,today_sunset = sunriseandsunset(n,longitude,latitude,altitude)
    #sunrise fraction should be 0.654167 / sunset should be 1.329618
    print("today_sunrise=",today_sunrise,today_sunrise-int(today_sunrise),"today_sunset=", today_sunset,today_sunset-int(today_sunset))
    tomorrow_sunrise,tomorrow_sunset = sunriseandsunset(n+1,longitude,latitude,altitude)
    print("tomorrow_sunrise=",tomorrow_sunrise,"tomorrow_sunset=",tomorrow_sunset)
    if (n+dfrac)>today_sunrise:
        next_sunrise=tomorrow_sunrise
    else:
        next_sunrise=today_sunrise
    if (n+dfrac) > today_sunset:
        next_sunset=tomorrow_sunset
    else:
        next_sunset=today_sunset
    print("next_sunrise=",next_sunrise,"next_sunset=", next_sunset)
    print(status)
    print("(n+dfrac) > today_sunrise :",(n+dfrac) > today_sunrise)
    print("(n+dfrac) < today_sunset :",(n+dfrac) < today_sunset)
    print("(n+dfrac) > today_sunset :",(n+dfrac) > today_sunset)
    print("(n+dfrac) < next_sunrise :",(n+dfrac) < next_sunrise)
    if (n+dfrac) > today_sunrise and (n+dfrac) < today_sunset and status==0:
		#door.open()
		status=1
		next_sunrise = tomorrow_sunrise
		timetowait=(next_sunset-(n+dfrac))*24*60*60
		print("Block door.open()")
        #print("door status=",status, "next_sunrise=",next_sunrise,"next_sunset=",next_sunset, "timetowait=",timetowait,"next_sunset-n=",next_sunset-n)
		time.sleep(timetowait)#5)
    elif (n+dfrac) > today_sunset and (n+dfrac) < next_sunrise and status==1:
		#door.close()
		status=0
		next_sunset = tomorrow_sunset
		timetowait=(next_sunrise-(n+dfrac))*24*60*60
		print("Block door.close()")
        #print("door status=",status, "next_sunrise=",next_sunrise,"next_sunset=",next_sunset, "timetowait=",timetowait,"next_sunset-n=",next_sunset-n)
		time.sleep(timetowait)#5)
    elif (n+dfrac) < today_sunrise and (n+dfrac) < next_sunset and status==1:
		#door.close()
		status=0
		timetowait=(next_sunrise-(n+dfrac))*24*60*60
		print("Block door.close if before sunrise")
        #print("door status=",status, "next_sunrise=",next_sunrise,"next_sunset=",next_sunset, "timetowait=",timetowait,"next_sunset-n=",next_sunset-n)
		time.sleep(timetowait)#5)
    else:
		timetowait=(min(next_sunrise, next_sunset)-(n+dfrac))*24*60*60
		print("timetowait=",timetowait)
		print("Block wait a bit more")
		time.sleep(timetowait+60)
