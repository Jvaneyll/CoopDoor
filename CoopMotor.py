#init libraries
import board
from digitalio import DigitalInOut, Direction, Pull
import busio
import pulseio
import time
 
##INIT
#init pins on board
PWM_pin= pulseio.PWMOut(board.D3, frequency=5000, duty_cycle=0)
FW_pin=DigitalInOut(board.D1)
FW_pin.direction = Direction.OUTPUT
RV_pin=DigitalInOut(board.D4)
RV_pin.direction = Direction.OUTPUT

# Safety checks
## Motor in stopped mode
PWM_pin.duty_cycle=0
FW_pin.value=0
RV_pin.value=0

#Create motor control function through H bridge
## Sens de rotation du moteur
STOP = 1
FWD = 2
REV = 3
## Duty cycles
FW_runtime = 15
RV_runtime = 15
FW_dc=100
RV_dc=100

##FUNCTION DEFINITION		
def MotDir(rot):
	""" Define rotation direction for motor """
	if(rot == FWD):
		FW_pin.value=True
		RV_pin.value=False
	elif(rot == REV):
		FW_pin.value=False
		RV_pin.value=True
	elif(rot == STOP):
		FW_pin.value=False
		RV_pin.value=False

def Inactive():
	""" Deactivate H bridge """
	PWM_pin.duty_cycle=0
	MotDir(1)

def Active(dc):
	""" Activate H bridge """
	PWM_pin.duty_cycle = int(dc * 65535 / 100)
    
def opendoor(dc,runtime):
    Inactive()
    MotDir(2)
    Active(dc)
    time.sleep(runtime)
    Inactive()

def closedoor(dc,runtime):
    Inactive()
    MotDir(3)
    Active(dc)
    time.sleep(runtime)
    Inactive()

for i in range(1,10,1):
	Inactive()
	closedoor(RV_dc,RV_runtime)
	time.sleep(2)
	opendoor(FW_dc,FW_runtime)
