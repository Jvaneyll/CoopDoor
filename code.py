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

##INIT I2C CONNECTION ON RTC AND GET CURRENT DATE
i2c = busio.I2C(board.SCL, board.SDA,frequency=400000)
rtc = adafruit_pcf8523.PCF8523(i2c)
if 'i2c' in locals() and 'rtc' in locals():
    now = rtc.datetime
    print(now)
else:
    print("i2c bus and RTC not initialized !")
    quit()

##INIT VARIABLES
longitude=4.677301 #West
latitude=50.645144 #North
Status=1 #(Door open by default at start)
print(longitude,latitude)
    
##DEFINE FUNCTIONS
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

def sunriseandsunset(n):
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
    H = acos((sinrad(-0.83+sqrt(150)/60*-2.076)-sinrad(latitude)*sinrad(delta))/(cosrad(latitude)*cosrad(delta)))*180/pi
    print(n,jtransit,H)
    #Calculate julian sunrise and sunset from 01/01/2000 by adding/substracting Hour angle from zenith position
    jset=jtransit + (H/360) + 0.020833
    #0.020833 is 30 min in fraction of julian day
    jrise=jtransit - (H/360)
    return (jrise, jset)
    
def nextsunriseandsusnset(n):
    today_sunrise,today_sunset = sunriseandsunset(n)
    tomorrow_sunrise,tomorrow_sunset = sunriseandsunset(n+1)
    print (today_sunrise)
    print(type(today_sunrise))
    print(today_sunset)
    print(type(today_sunset))
    
    print (tomorrow_sunrise, tomorrow sunset)
    
    if n > today_sunrise:
		next_sunrise=todaysunriseandsunset(n+1)
	else:
		next_sunrise=today_sunrise
	if n > today_sunset:
		next_sunset=todaysunriseandsunset(n+1)
	else:
		next_sunset=today_sunset
		
	print(next_sunrise, next_sunset)
	return(next_sunrise, next_sunset)

##RUN PROGRAM
# While True:
	# now = rtc.datetime
	# n=calcjuliandate2000(now)
	# today_sunrise,today_sunset = sunriseandsunset(n)
	# if n > today_sunrise and n < next_sunset:
		# door.open()
		# status=1
		# next_sunrise, next_sunset = nextsunriseandsusnset(n)
		# timetowait=(next_sunset-n)*24*60*60
		# time.sleep(timetowait)
	# elif n > today_sunset and n < next_sunrise:
		# door.close()
		# status=0
		# next_sunrise, next_sunset = nextsunriseandsusnset(n)
		# timetowait=(next_sunrise-n)*24*60*60
		# time.sleep(timetowait)
	# else:
		# timetowait=(min(next_sunrise, next_susnset)-n)*24*60*60
		# time.sleep(timetowait)

def main():
	now = rtc.datetime
	n=calcjuliandate2000(now)
	today_sunrise,today_sunset = sunriseandsunset(n)
	print(now, n, today_sunrise, today_sunset)
	if n > today_sunrise and n < next_sunset:
		#door.open()
		status=1
		next_sunrise, next_sunset = nextsunriseandsusnset(n)
		timetowait=(next_sunset-n)*24*60*60
		print(status, next_sunrise, next_sunset, timetowait)
		time.sleep(5)
	elif n > today_sunset and n < next_sunrise:
		#door.close()
		status=0
		next_sunrise, next_sunset = nextsunriseandsusnset(n)
		timetowait=(next_sunrise-n)*24*60*60
		print(status, next_sunrise, next_sunset, timetowait)
		time.sleep(5)
	else:
		timetowait=(min(next_sunrise, next_susnset)-n)*24*60*60
		print(timetowait)
		time.sleep(5)
	
    
if __name__ == '__main__':
    main()
