import pyb
from pyb import Pin, Timer, ADC, DAC, LED
from array import array			# need this for memory allocation to buffers
from oled_938 import OLED_938	# Use OLED display driver
from audio import MICROPHONE
from neopixel import NeoPixel
from Neopixy import Neopixy
import micropython


micropython.alloc_emergency_exception_buf(100)


#------------------------------------------------------------------

#INITIALISING OLED SCREEN

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
i2c = pyb.I2C(2, pyb.I2C.MASTER)
devid = i2c.scan()				# find the I2C device number
oled = OLED_938(
    pinout={"sda": "Y10", "scl": "Y9", "res": "Y8"},
    height=64,
    external_vcc=False,
    i2c_devid=i2c.scan()[0],
)
oled.poweron()
oled.init_display()
oled.draw_text(0,0, 'Dance Baby')
oled.display()

#------------------------------------------------------------------

#NEOPIXEL

# create neopixel object
np = NeoPixel(Pin("Y12", Pin.OUT), 8)


#------------------------------------------------------------------

#INTERRUPT MICROPHONE STUFF

# Create timer interrupt - one every 1/8000 sec or 125 usec
pyb.disable_irq()
sample_timer = pyb.Timer(7, freq=8000)	# set timer 7 for 8kHz

N = 160				# number of sample to calculate instant energy
mic = ADC(Pin('Y11'))
audio = MICROPHONE(sample_timer, mic, N)
pyb.enable_irq(True)

# Calculate energy over 50 epochs, each 20ms (i.e. 1 sec)
M = 50						# number of instantaneous energy epochs to sum
MIN_BEAT_PERIOD = 500	# no beat less than this

# initialise variables for main program loop
e_ptr = 0					# pointer to energy buffer
e_buf = array('L', 0 for i in range(M))	# reserve storage for energy buffer
sum_energy = 0				# total energy in last 50 epochs
oled.draw_text(0,20, 'Kishore Da (_*_)')	# Useful to show what's happening
oled.display()
pyb.delay(100)
tic = pyb.millis()			# mark time now in msec


#------------------------------------------------------------------

#MOTOR INITIALISATION

# Define pins to control motor
A1 = Pin('X3', Pin.OUT_PP)		# Control direction of motor A
A2 = Pin('X4', Pin.OUT_PP)
PWMA = Pin('X1')				# Control speed of motor A
B1 = Pin('X7', Pin.OUT_PP)		# Control direction of motor B
B2 = Pin('X8', Pin.OUT_PP)
PWMB = Pin('X2')				# Control speed of motor B

# Configure timer 2 to produce 1KHz clock for PWM control
tim = Timer(2, freq = 1000)
motorA = tim.channel (1, Timer.PWM, pin = PWMA)
motorB = tim.channel (2, Timer.PWM, pin = PWMB)

# Define 5k Potentiometer
pot = pyb.ADC(Pin('X11'))


#MOTOR FUNCTIONS

def A_forward(value):
	A1.low()
	A2.high()
	motorA.pulse_width_percent(value)

def A_back(value):
	A2.low()
	A1.high()
	motorA.pulse_width_percent(value)
	
def A_stop():
	A1.high()
	A2.high()
	
def B_forward(value):
	B2.low()
	B1.high()
	motorB.pulse_width_percent(value)

def B_back(value):
	B1.low()
	B2.high()
	motorB.pulse_width_percent(value)
	
def B_stop():
	B1.high()
	B2.high()
	
# Initialise variables
speed = 0
A_speed = 0
A_count = 0
B_speed = 0
B_count = 0


#MOTOR DANCE
def dance_move(current_dance_move):

		if current_dance_move == 'F' : #Move forward

			A_forward(50)
			B_forward(50)
			pyb.delay(500)

		elif current_dance_move == 'B' : #Move backwards

			A_back(50)
			B_back(50)
			pyb.delay(500)

		elif current_dance_move == 'L': #Spin counter-clockwise

			A_forward(50)
			B_back(10)
			pyb.delay(500)

		elif current_dance_move == 'R' :#Spin clockwise

			A_forward(10)
			B_back(50)
			pyb.delay(500)

#------------------------------------------------------------------

#CALLING THE DANCE MOVES FROM TEXT

dance_move_list=[]
with open('dance.txt','r') as f: 
	lines = f.read()
	# dance_move_list.append(str(lines).strip('\n').split('\n'))
	dance_move_list = str(lines).strip('\n').split('\n')
# print(lines)
print(dance_move_list)
counter=0

#------------------------------------------------------------------

#WHILE LOOP STUFF

while True:			# Main program loop
	if audio.buffer_is_filled():		# semaphore signal from ISR - set if buffer is full
		
		# Fetch instantaneous energy
		E = audio.inst_energy()			# fetch instantenous energy
		audio.reset_buffer()			# get ready for next epoch

		# compute moving sum of last 50 energy epochs with circular buffer
		sum_energy = sum_energy - e_buf[e_ptr] + E
		e_buf[e_ptr] = E			# over-write earliest energy with most recent
		e_ptr = (e_ptr + 1) % M		# increment e_ptr with wraparound - 0 to M-1
		average_energy = sum_energy/M

		# Compute ratio of instantaneous energy/average energy
		c = E/average_energy

		
		if (pyb.millis()-tic > MIN_BEAT_PERIOD):	# if longer than minimum period
			
			
			if (c<0.3):
				Neopixy.neo_group1()
				tic = pyb.millis()
			if (0.3<c<0.5):
				Neopixy.neo_group2()
				tic = pyb.millis()
			if (0.5<c<0.8):
				Neopixy.neo_group3()
				tic = pyb.millis()
			if (0.8<c<2.0):
				Neopixy.neo_group4()
				tic = pyb.millis()
			if (2.0<c<2.5):
				Neopixy.neo_group5()
				tic = pyb.millis()
			if (2.5<c<2.7):
				Neopixy.neo_group6()
				tic = pyb.millis()
			if (2.8<c<3.1):
				Neopixy.neo_group7()
				tic = pyb.millis()
			if (3.1<c<5.3):
				Neopixy.neo_group8()
				tic = pyb.millis()
	
			if (c>1.8):
				current_dance_move=dance_move_list[counter]
				counter = counter + 1
				dance_move(dance_move_list[counter])
				print(dance_move_list[counter])
				print(counter)

				if counter==(len(dance_move_list)-1):
					counter=0
					print(dance_move_list[counter])
					print(counter)
					dance_move(dance_move_list[counter])

		buffer_full = False
