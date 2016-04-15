import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)

inputPin=19
outputPin=26

gpio.setup(inputPin,gpio.IN,pull_up_down=gpio.PUD_DOWN)
gpio.setup(outputPin,gpio.OUT)

gpio.output(outputPin,True)
try:

	while True:
		if gpio.input(inputPin)==False:
			print "False"
		else:
			print "True"
except KeyboardInterrupt:
	gpio.cleanup()
