# -*- coding: utf-8 -*-

import RPi.GPIO as gpio


matrix=[[1,2,3],
	[4,5,6],
	[7,8,9],
	['*',0,'#']]

rows=(12,16,20,21)
cols=(25,8,7)

gpio.setmode(gpio.BCM)

for row in rows:
	gpio.setup(row,gpio.IN,pull_up_down=gpio.PUD_UP)
for col in cols:
	gpio.setup(col,gpio.OUT)
	gpio.output(col,True)



try:
	while True:
		for j in xrange(0,3,1):
			gpio.output(cols[j],False)
			
			for i in xrange(0,4,1):
				if gpio.input(rows[i])==0:
					print matrix[i][j]
					while gpio.input(rows[i])==0:
						pass

			gpio.output(cols[j],True)


except KeyboardInterrupt:
	gpio.cleanup()




