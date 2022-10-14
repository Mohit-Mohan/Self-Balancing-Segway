import pyb
from pyb import Pin, Timer, ADC, LED
from oled_938 import OLED_938	# Use OLED display driver
from mpu6050 import MPU6050
from PID import PIDC
import time

#------------------------------------------------------------------

#INITIALISING OLED SCREEN
# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
i2c = pyb.I2C(2, pyb.I2C.MASTER)
devid = i2c.scan()				# find the I2C device number
oled = OLED_938(
    pinout={"sda": "Y10", "scl": "Y9", "res": "Y8"},
    height=64, external_vcc=False, i2c_devid=i2c.scan()[0],
)
oled.poweron()
oled.init_display()

#------------------------------------------------------------------

#INITIALIZING IMU DEVICE
# IMU connected to X9 and X10
imu = MPU6050(1, False)    	# Use I2C port 1 on Pyboard

def roll_angle():
	roll = int(imu.roll())
	return roll

def pitch_angle():
	pitch = int(imu.pitch())
	return pitch

def pitch_rate():
	pitch_rate = int(imu.get_gy())
	return pitch_rate

def pitch_estimate(pitch, dt, alpha):
    theta = imu.pitch()
    pitch_dot = imu.get_gy()
    pitch = alpha*(pitch + pitch_dot*dt*0.001) + (1-alpha)*theta
    return pitch

#------------------------------------------------------------------

#INITIALSING MOTOR
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

def A_forward(value):
	A1.low()
	A2.high()
	motorA.pulse_width_percent(value)

def A_back(value):
	A2.low()
	A1.high()
	motorA.pulse_width_percent(value)
	
def B_forward(value):
	B2.low()
	B1.high()
	motorB.pulse_width_percent(value)

def B_back(value):
	B1.low()
	B2.high()
	motorB.pulse_width_percent(value)
	
# Initialise variables
A_speed = 0
B_speed = 0

#------------------------------------------------------------------

# TUNING PID VALUES
# Define 5k Potentiometer
pot = pyb.ADC(Pin('X11'))


kp = 5
kd = 0.3
ki = 60
theta_0 = 0 # calibrated value of no tilt

PID = PIDC(kp, kd, ki, theta_0)

tic = pyb.millis()

while True:
    toc = pyb.millis()

    # pitch angle estimate
    pitch = pitch_angle()
    dt = toc - tic
    alpha = 0.77
    pitch_guess = pitch_estimate(pitch, dt, alpha)
    pitch_dot = pitch_rate()
    
    tic = pyb.millis()
    # pid output value
    output = PID.get_pwm(pitch_guess, pitch_dot)
    if(output > 0):
        A_back(abs(output))
        B_back(abs(output))
    else:
        A_forward(abs(output))
        B_forward(abs(output))
	
    PID.target_reset()