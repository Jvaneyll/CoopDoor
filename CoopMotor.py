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
FW_pin.pull = Pull.DOWN
RV_pin=DigitalInOut(board.D4)
RV_pin.direction = Direction.OUTPUT
RV_pin.pull = Pull.DOWN

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
FW_dc=100
RV_dc=100

##FUNCTION DEFINITION

def Inactive():
	""" Deactivate H bridge """
	PWM_pin.duty_cycle=0
	FW_pin.value=0
	RV_pin.value=0
		
def MotDir(rot):
	""" Define rotation direction for motor """
	if(rot == FWD):
		FW_pin.value=1
		RV_pin.value=0
	elif(rot == REV):
		FW_pin.value=0
		RV_pin.value=1
	elif(rot == STOP):
		FW_pin.value=0
		RV_pin.value=0


def Active(dc):
	""" Activate H bridge """
	PWM_pin.duty_cycle = int(dc * 65535 / 100)
	
		
if __name__ == '__main__':
	Inactive()
	Forward(30)
	Reverse(30)
	Left(30)
	Right(30)
	Inactive()
	GPIO.cleanup()


##RUN SCRIPT
while True:
    for i in range(100):
        # PWM LED up and down
        if i < 50:
            PWM_pin.duty_cycle = int(i * 2 * 65535 / 100)  # Up
        else:
            PWM_pin.duty_cycle = 65535 - int((i - 50) * 2 * 65535 / 100)  # Down
        time.sleep(0.01)



