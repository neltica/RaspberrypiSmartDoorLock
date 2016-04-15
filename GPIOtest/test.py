import RPi.GPIO as gpio
import time

out=23

gpio.setmode(gpio.BCM)

gpio.setup(out,gpio.OUT)

gpio.output(out,True)	
time.sleep(10)
gpio.output(out,False)
gpio.cleanup()
