import RPi.GPIO as gpio
import time

out=13
out2=6

gpio.setmode(gpio.BCM)

gpio.setup(out,gpio.OUT)

gpio.setup(out2,gpio.OUT)

try:
	gpio.output(out,True)
	gpio.output(out2,True)
	while True:
		print "true"
#	gpio.output(out,True)	
#	time.sleep(0.001)
#		print "output"
#		gpio.output(out,False)
except KeyboardInterrupt:
	gpio.cleanup()
