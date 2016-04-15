# -*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


import RPi.GPIO as gpio

import time

import picamera
import threading


#pin setting
rows=(12,16,20,21)
cols=(25,8,7)
trig=23
echo=24
doorCheckPinIn=19
doorCheckPinOut=26


#pw setting
doorLockPW=[0,0,0,0]


def allGPIOSet():

	global rows
	global cols
	global trig
	global echo

	gpio.setmode(gpio.BCM)


	gpio.setup(trig,gpio.OUT)
	gpio.setup(echo,gpio.IN)


	for row in rows:
		gpio.setup(row,gpio.IN,pull_up_down=gpio.PUD_UP)
	for col in cols:
		gpio.setup(col,gpio.OUT)
		gpio.output(col,True)

	gpio.setup(doorCheckPinIn,gpio.IN,pull_up_down=gpio.PUD_DOWN)
	gpio.setup(doorCheckPinOut,gpio.OUT)
	gpio.output(doorCheckPinOut,True)



def cameraOpen():
	print "camera open"

def cameraClose():
	print "camera close"

def cameraCapture():
	print "camera capture"
	with picamera.PiCamera() as camera:
		camera.capture('./image.jpg')

def doorCheck():
	startTime=time.localtime().tm_min
	while True:
		if not areYouMaster and endNumbering:
			cameraOpen()
			cameraCapture()
			cameraClose()
		else:
			if time.localtime().tm_min-startTime>=1:
				break
			

def distanceCheck():
	global trig
	global echo
	print "start"

	try:
#	while True:
		gpio.output(trig,False)
		time.sleep(0.5)
		gpio.output(trig,True)
		time.sleep(0.00001)
		gpio.output(trig,False)
		while gpio.input(echo)==0:
			pulse_start=time.time()
		while gpio.input(echo)==1:
			pulse_end=time.time()
		pulse_duration=pulse_end-pulse_start
		distance=pulse_duration*17000
		distance=round(distance,2)
		print "distance : ",distance,"cm"
		return distance
#				subject=raw_input('subject:')
#				sender=raw_input('from:')
#				receiver=raw_input('receiver:')
#				text=raw_input('text:')
#				fileName=raw_input("filename:")
#				gmailID=raw_input('gmailID:')
#				gmailPW=raw_input('gmailPW')
#				emailSend(subject,sender,receiver,text,gmailID,gmailPW)
	except:
		print "distanceCheck error"
		gpio.cleanup()
		exit()

def emailSend(subject='',sender='',recevier='',text='',filename='',gmailID='',gmailPW=''):
	msg=MIMEMultipart()
	msg['Subject']=subject
	msg['From']=sender
	msg['To']=recevier


	file=open(filename,'rb')
	img=MIMEImage(file.read())
	file.close()
	msg.attach(img)

	txt=MIMEText(text)
	msg.attach(txt)


	s=smtplib.SMTP('smtp.gmail.com',587)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login(gmailID,gmailPW)
	s.sendmail(gmailID,[recevier],msg.as_string())
	s.quit()


def doorLockInput():
	global rows
	global cols


	matrix=[[1,2,3],
		[4,5,6],
		[7,8,9],
		['*',0,'#']]


	try:
		for j in xrange(0,3,1):
			gpio.output(cols[j],False)
			
			for i in xrange(0,4,1):
				if gpio.input(rows[i])==0:
					print matrix[i][j]
					while gpio.input(rows[i])==0:
						pass
					return matrix[i][j]
			gpio.output(cols[j],True)


		return None
	except KeyboardInterrupt:
		gpio.cleanup()
		exit()


def handleCheck():
	return gpio.input(doorCheckPinIn)


def main():
	try:
		inputs=[]
		allGPIOSet()
		while True:
			if distanceCheck()<20:
				while True:
					if handleCheck():
						cameraOpen()
						cameraCapture()
						cameraClose()
					data=doorLockInput()
					breakCheck=False
					time.sleep(0.01)
					if data=='*':
						while True:
							if handleCheck():
								cameraOpen()
								cameraCapture()
								cameraClose()
							data=doorLockInput()
							if data=='*':
								if inputs==doorLockPW:
									print "pass"
								else:
									cameraOpen()
									cameraCapture()
									cameraClose()
									print "error"
								inputs=[]
								breakCheck=True
								break
							elif data!=None:
								inputs.append(data)
							time.sleep(0.01)
					if breakCheck:
						break
	except KeyboardInterrupt:
	     gpio.cleanup()

if __name__=="__main__":
	main()
