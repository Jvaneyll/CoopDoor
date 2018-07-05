##DESCRIPTION
# The objective of this script is to control a DC motor (via H bridge logic) at every sunrise and sunset using the Trinket M0 controller board and an I2C-connected Real Time Controller (RTC) module.
# The RTC module is PCF8523 and has been initialized on a Rpi3B upfront.

##INIT LIBRARIES
import math
from math import floor

##INIT VARIABLES

##INIT I2C connection

##FUNCTIONS DEFINITIONS

#Sunrise/-set calculation


# create wrapped trig functions which operate on degrees
def make_degree(f):
  return lambda x: math.degrees(f(math.radians(x)))

d_cos  = make_degree(math.cos)
d_sin  = make_degree(math.sin)
d_tan  = make_degree(math.tan)
d_atan = make_degree(math.atan)
d_asin = make_degree(math.asin)
d_acos = make_degree(math.acos)

def main():

  # date of interest
  day, month, year = 6, 7, 2018

  # local UTC offset
  localOffset = +2

  # NOTE: longitude is positive for East and negative for West
  latitude, longitude = 50.645144, 4.677301

  # Sun's zenith for sunrise/sunset
  zenith = 90

  # get rising time. Will get setting time if this is false
  rising = 0

  # 1. first calculate the day of the year
  N1 = floor(275 * month / 9)
  N2 = floor((month + 9) / 12)
  N3 = (1 + floor((year - 4 * floor(year / 4) + 2) / 3))
  N = N1 - (N2 * N3) + day - 30

  # 2. convert the longitude to hour value and calculate an approximate time
  lngHour = longitude / 15
  if rising:
    t = N + ((6 - lngHour) / 24)
  else:
    t = N + ((18 - lngHour) / 24)

  # 3. calculate the Sun's mean anomaly
  M = (0.9856 * t) - 3.289


  # adjust into the specified range
  # rng must be a list of 2 values [bottom, top]
  def adjust(x, rng=None):
    if not isinstance(rng, list) or len(rng) != 2:
      raise Exception("invalid range")

    bottom, top = rng[0], rng[1]

    if x < bottom:
      x = x + top
    elif x > top:
      x = x - top

    return x

  # 4. calculate the Sun's true longitude
  L = M + (1.916 * d_sin(M)) + (0.020 * d_sin(2 * M)) + 282.634
  L = adjust(L, rng=[0, 360])

  # 5a. calculate the Sun's right ascension
  RA = d_atan(0.91764 * d_tan(L))
  RA = adjust(RA, rng=[0, 360])

  # 5b. right ascension value needs to be in the same quadrant as L
  Lquadrant = (floor(L / 90)) * 90
  RAquadrant = (floor(RA / 90)) * 90
  RA = RA + (Lquadrant - RAquadrant)

  # 5c. right ascension value needs to be converted into hours
  RA = RA / 15

  # 6. calculate the Sun's declination
  sinDec = 0.39782 * d_sin(L)
  cosDec = d_cos(d_asin(sinDec))

  # 7a. calculate the Sun's local hour angle
  cosH = (d_cos(zenith) - (sinDec * d_sin(latitude))) / (cosDec * d_cos(latitude))
  
  if rising and cosH > 1:
    raise Exception("the sun never rises on this location (on the specified date)")
  if not rising and cosH < -1:
    raise Exception("the sun never sets on this location (on the specified date)")

  # 7b. finish calculating H and convert into hours
  if rising:
    H = 360 - d_acos(cosH)
  else:
    H = d_acos(cosH)

  H = H / 15
  
  # 8. calculate local mean time of rising/setting
  T = H + RA - (0.06571 * t) - 6.622

  # 9. adjust back to UTC
  UT = T - lngHour
  UT = adjust(UT, rng=[0, 24])

  # 10. convert UT value to local time zone of latitude/longitude
  localT = UT + localOffset

  if rising:
    print("sunrise {}".format(localT))
  else:
    print("sunset {}".format(localT))


if __name__ == '__main__':
    main()

#Calculate next sunrise

#Calculate next sunset

#Open door

#Close door

##INIT BOARD AND STATUS

##RUN PROGRAM
