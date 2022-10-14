import pyb
from pyb import Pin, Timer, ADC
from oled_938 import OLED_938	# Use OLED display driver
from mpu6050 import MPU6050


# Define pins to control motor
A1 = Pin('X3', Pin.OUT_PP)		# Control direction of motor A
A2 = Pin('X4', Pin.OUT_PP)
PWMA = Pin('X1')				# Control speed of motor A
B1 = Pin('X7', Pin.OUT_PP)		# Control direction of motor B
B2 = Pin('X8', Pin.OUT_PP)
PWMB = Pin('X2')				# Control speed of motor B

imu = MPU6050(1, False)  

# Configure timer 2 to produce 1KHz clock for PWM control
tim = Timer(2, freq = 1000)
motorA = tim.channel (1, Timer.PWM, pin = PWMA)
motorB = tim.channel (2, Timer.PWM, pin = PWMB)

# Define 5k Potentiometer
pot = pyb.ADC(Pin('X11'))

# I2C connected to Y9, Y10 (I2C bus 2) and Y11 is reset low active
i2c = pyb.I2C(2, pyb.I2C.MASTER)
devid = i2c.scan()				# find the I2C device number
oled = OLED_938(
    pinout={"sda": "Y10", "scl": "Y9", "res": "Y8"},
    height=64, external_vcc=False, i2c_devid=i2c.scan()[0],
)
oled.poweron()
oled.init_display()
oled.display()

trigger = pyb.Switch()
while not trigger():
	time.sleep(0.001)
while trigger(): pass

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

#-------  Section to set up Interrupts ----------
def isr_motorA(dummy):	# motor A sensor ISR - just count transitions
	global A_count
	A_count += 1

def isr_motorB(dummy):	# motor B sensor ISR - just count transitions
	global B_count
	B_count += 1
		
def isr_speed_timer(dummy): 	# timer interrupt at 100msec intervals
	global A_count
	global A_speed
	global B_count
	global B_speed
	A_speed = A_count			# remember count value
	B_speed = B_count
	A_count = 0					# reset the count
	B_count = 0
	
# Create external interrupts for motorA Hall Effect Senor
import micropython
micropython.alloc_emergency_exception_buf(100)
from pyb import ExtInt

motorA_int = ExtInt ('Y4', ExtInt.IRQ_RISING, Pin.PULL_NONE,isr_motorA)
motorB_int = ExtInt ('Y6', ExtInt.IRQ_RISING, Pin.PULL_NONE,isr_motorB)

# Create timer interrupts at 100 msec intervals
speed_timer = pyb.Timer(4, freq=10)
speed_timer.callback(isr_speed_timer)

#-------  END of Interrupt Section  ----------

def read_imu_pitch(dt): #defining a function called read_imu

    global g_pitch
    alpha = 0.77    # larger = longer time constant
    pitch = int(imu.pitch()) # this is a defined method in mpu6050.py
    g_pitch = int(alpha*(g_pitch + imu.get_gy()*dt*0.001) + (1-alpha)*pitch) #complementary filter pitch angle
    return g_pitch

g_pitch = 0  
tic = pyb.millis()	

class PIDC:
    def __init__(self, Kp, Kd, Ki):
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.error_last = 0       # These are global variables to remember various states of controller
        self.tic = pyb.millis()
        self.error_sum = 0

    def getPWM(self, target, speed):

        # error input
        error = target - speed                      # e[n]
    
        # derivative input
        derivative = error - self.error_last        # error_dot. assume dt is constant
                                                    # 1/dt is absorbed into Kd
                                                    # this avoid division by small value

        toc = pyb.millis()
        dt = (toc-self.tic)*0.001                   # find dt as close to when used as possible
        # Integral input 
        self.error_sum += error*dt            
 
        #   Output 
        PID_output = (self.Kp * error) + (self.Ki * self.error_sum) + (self.Kd * derivative)

        # Store previous values 
        self.error_last = error
        self.tic = toc

        pwm_out = min(abs(PID_output), 100)         # Make sure pwm is less than 100 

        return pwm_out

pid = PIDC(6.3, 20, 0.8)

while True:

	toc = pyb.millis()

	pitch_measured = read_imu_pitch(toc-tic)
	pitch_dot_measured = imu.get_gy()
	
	if (pid.getPWM(0.0, pitch_measured) >= 0):		# forward
		A_forward(pid.getPWM(0.0, pitch_measured))
		B_forward(pid.getPWM(0.0, pitch_measured))
	else:
		A_back(abs(pid.getPWM(0.0, pitch_measured)))
		B_back(abs(pid.getPWM(0.0, pitch_measured)))
	
	oled.draw_text(0,20,'Motor A:{:5.2f} rps'.format(A_speed/39))	
	oled.draw_text(0,30,'Motor B:{:5.2f} rps'.format(B_speed/39))	
	oled.display()
	
	pyb.delay(10)
	tic = pyb.millis()