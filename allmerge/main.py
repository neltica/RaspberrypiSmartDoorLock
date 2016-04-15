# -*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText


import RPi.GPIO as gpio
import time


import time
import picamera

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
#check door source position
		if not areYouMaster and endNumbering:
			cameraOpen()
			cameraCapture()
			cameraClose()
		else:
			if time.localtime().tm_min-startTime>=1:
				break
			

def distanceCheck():
	gpio.setmode(gpio.BCM)

	trig=23
	echo=24

	print "start"

	gpio.setup(trig,gpio.OUT)
	gpio.setup(echo,gpio.IN)

	try:
		while True:
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
			if distance<20:
				cameraOpen()
				time.sleep(10)
				cameraCapture()
				cameraClose()
				subject=raw_input('subject:')
				sender=raw_input('from:')
				receiver=raw_input('receiver:')
				text=raw_input('text:')
				fileName=raw_input("filename:")
				gmailID=raw_input('gmailID:')
				gmailPW=raw_input('gmailPW')
				emailSend(subject,sender,receiver,text,gmailID,gmailPW)
	except:
		gpio.cleanup()

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



def main():
	distanceCheck()


if __name__=="__main__":
	main()
