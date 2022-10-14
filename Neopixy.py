'''
Python Class which defines the behaviour of the neopixel depending on different beats.
'''
import pyb
from neopixel import NeoPixel
from pyb import Pin

np = NeoPixel(Pin("Y12", Pin.OUT), 8)

class Neopixy:


    def neo_group1():		
        np[0] = (148, 85, 244)
        np.write()

        pyb.delay(75)

        np[0] = (0, 0, 0)
        np.write()

        pyb.delay(1)

    def neo_group2():

        np[0] = (148, 85, 244)
        np.write()
        pyb.delay(50)
        np[1] = (133, 77, 220)
        np.write()

        pyb.delay(75)

        np[0] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[1] = (0, 0, 0)
        np.write()

        pyb.delay(1)

    def neo_group3():

        np[0] = (148, 85, 244)
        np.write()
        pyb.delay(50)
        np[1] = (133, 77, 220)
        np.write()
        pyb.delay(50)
        np[2] = (118, 68, 195)
        np.write()

        pyb.delay(75)

        np[0] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[1] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[2] = (0, 0, 0)
        np.write()

        pyb.delay(1)

    def neo_group4():

        np[0] = (148, 85, 244)
        np.write()
        pyb.delay(50)
        np[1] = (133, 77, 220)
        np.write()
        pyb.delay(50)
        np[2] = (118, 68, 195)
        np.write()
        pyb.delay(50)
        np[3] = (104, 59, 171)
        np.write()

        pyb.delay(75)

        np[0] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[1] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[2] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[3] = (0, 0, 0)
        np.write()

        pyb.delay(1)

    def neo_group5():

        np[0] = (148, 85, 244)
        np.write()
        pyb.delay(50)
        np[1] = (133, 77, 220)
        np.write()
        pyb.delay(50)
        np[2] = (118, 68, 195)
        np.write()
        pyb.delay(50)
        np[3] = (104, 59, 171)
        np.write()
        np[4] = (89, 51, 146)
        np.write()

        pyb.delay(75)

        np[0] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[1] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[2] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[3] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[4] = (0, 0, 0)
        np.write()

        pyb.delay(1)

    def neo_group6():

        np[0] = (148, 85, 244)
        np.write()
        pyb.delay(50)
        np[1] = (133, 77, 220)
        np.write()
        pyb.delay(50)
        np[2] = (118, 68, 195)
        np.write()
        pyb.delay(50)
        np[3] = (104, 59, 171)
        np.write()
        np[4] = (89, 51, 146)
        np.write()
        pyb.delay(50)
        np[5] = (74, 43, 122)
        np.write()

        pyb.delay(75)

        np[0] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[1] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[2] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[3] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[4] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[5] = (0, 0, 0)
        np.write()
        pyb.delay(1)

    def neo_group7():

        np[0] = (148, 85, 244)
        np.write()
        pyb.delay(50)
        np[1] = (133, 77, 220)
        np.write()
        pyb.delay(50)
        np[2] = (118, 68, 195)
        np.write()
        pyb.delay(50)
        np[3] = (104, 59, 171)
        np.write()
        np[4] = (89, 51, 146)
        np.write()
        pyb.delay(50)
        np[5] = (74, 43, 122)
        np.write()
        pyb.delay(50)
        np[6] = (38, 4, 51)
        np.write()

        pyb.delay(75)

        np[0] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[1] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[2] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[3] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[4] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[5] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[6] = (0, 0, 0)
        np.write()

        pyb.delay(1)

    def neo_group8():
        
        np[0] = (148, 85, 244)
        np.write()
        pyb.delay(50)
        np[1] = (133, 77, 220)
        np.write()
        pyb.delay(50)
        np[2] = (118, 68, 195)
        np.write()
        pyb.delay(50)
        np[3] = (104, 59, 171)
        np.write()
        np[4] = (89, 51, 146)
        np.write()
        pyb.delay(50)
        np[5] = (74, 43, 122)
        np.write()
        pyb.delay(50)
        np[6] = (38, 4, 51)
        np.write()
        pyb.delay(50)
        np[7] = (19, 2, 25)
        np.write()

        pyb.delay(75)

        np[0] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[1] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[2] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[3] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[4] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[5] = (0, 0, 0)
        np.write()
        pyb.delay(50)
        np[6] = (0, 0, 0)
        np.write()
        np[7] = (0, 0, 0)
        np.write()
        
        pyb.delay(1)