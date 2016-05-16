# -*- coding: utf-8 -*-

import smtplib #smtp 사용하기 위해서 포함
from email.mime.multipart import MIMEMultipart #MIMEMultipart 이미지랑 텍스트를 함께 보내려면 필요함.
from email.mime.image import MIMEImage    #이미지를 보내려면 필요함.
from email.mime.text import MIMEText     #텍스트를 보내려면 필요함.


import RPi.GPIO as gpio             # 판울 쓰려면 필요함

import time         # 시간함수 쓰기 위해서

import picamera           # 카메라 쓰려면 필요함

#pin setting
rows=(12,16,20,21)            #키패드
cols=(25,8,7)                 #키패드

trig=23            #초음파센서 트리거핀
echo=24        # 초음파센서 에코핀

handleCheckPinIn=19 #손잡이 돌아갔는지 확인하는 핀 암컷
handleCheckPinOut=26   #손잡이 돌아갔는지 확인하는 핀 숫컷

doorOnOff=13 # 도어락 제어핀

#pw setting
doorLockPW=[0,0,0,0]    # 도어락 초기 패스워드


def allGPIOSet():    # 핀 초기화
	print "all GPIO set"
	global rows
	global cols
	global trig
	global echo

	gpio.setmode(gpio.BCM)    #BCM방식에 맞춰서 GPIO핀 위치를 잡음.


	gpio.setup(trig,gpio.OUT)      #트리거 핀을 출력용으로 설정 (BCM기준으로 23번핀)
	gpio.setup(echo,gpio.IN)   #에코핀을 입력용핀으로 설정(BCM기준 24번핀)


	for row in rows:
		gpio.setup(row,gpio.IN,pull_up_down=gpio.PUD_UP)  #키패드의 행을 풀업다운 저항을 적용하여 입력용으로 설정한다.
	for col in cols:
		gpio.setup(col,gpio.OUT) # 키패드의 열을 출력용으로 설정한다.
		gpio.output(col,True)   # 출력을 시작한다.

	gpio.setup(handleCheckPinIn,gpio.IN,pull_up_down=gpio.PUD_DOWN)   #핸들핀을 입력용으로 설정하고 풀다운 저항으로 세팅한다. 암컷
	gpio.setup(handleCheckPinOut,gpio.OUT)       #핸들핀을 출력용으로 설정한다. 숫컷
	gpio.output(handleCheckPinOut,True)   #출력용 핀에서 출력을 시작한다.

	gpio.setup(doorOnOff,gpio.OUT)   #도어락 제어핀을 출력용으로 세팅한다.


def cameraOpen():   #카메라 오픈 함수
	print "camera open"

def cameraClose():   # 카메로 클로즈 함수
	print "camera close"

def cameraCapture():   # 카메라 사진찍는 함수
	print "camera capture"
	with picamera.PiCamera() as camera:
		camera.capture('./image.jpg')        #실제로 카메라 사진을 찍는 함수 image.jpg파일로 출력된다.

def doorOpen():
	print "door open"
	gpio.output(doorOnOff,True)        #도어락 제어핀에서 출력을 시작한다.
	time.sleep(0.1)   #0.1초 정도 멈춘다.
	gpio.output(doorOnOff,False)   #도어락 제어핀에서 출력을 멈춘다,
	pass

def distanceCheck():        #거리체크함수
	global trig
	global echo
	print "distance Check"

	try:
		gpio.output(trig,False)        #트리커핀에서 출력을 멈춘다,
		time.sleep(0.5)             #0.5초 출력을 유지했다가
		gpio.output(trig,True)       #트리거핀에서 출력한다.
		time.sleep(0.00001)          #0.00001초 멈췄다가
		gpio.output(trig,False)      #트리거 핀에서 출력을 멈춘다.
		while gpio.input(echo)==0:        #에코핀에서 입력이 안들어오면
			pulse_start=time.time()           #pulse_start변수에 현재 시간을 대입하면서 에코핀 입력으로 계속 반복한다.
		while gpio.input(echo)==1:      #에코핀에서 입력이 들어오면
			pulse_end=time.time()        #pulse_end변수에 현재시간을 대입하면서 에코핀에서 입력이 안들어올때까지 반복한다.
		pulse_duration=pulse_end-pulse_start         #입력들어오는게 종료되면 입력이 마지막으로 들어온 시간부터 입력이 마지막으로 안들어온 시간을 빼서 pulse_duration에 저장한다.
		distance=pulse_duration*17000    # pulse_duration에 17000을 곱해서 거리를 계산한다.
		distance=round(distance,2)          #거리를 소수점 둘째자리까지 표현한다.
		print "distance : ",distance,"cm"
		return distance                       #거리가 계산되면 리턴한다.
	except:
		print "distanceCheck error"
		gpio.cleanup()
		exit()

def emailSend(subject='',sender='',recevier='',text='',filename='',gmailID='',gmailPW=''):      #이메일 전송 함수


#subject 는 메일 제목
#sender는 보내는 사람 메일 주소
#recevier 는 받는사람 메일주소
#text는 내용
#filename 이미지 파일 이름  image.jpg로 고정할것
#gmailID 는 지메일 아이디
#gmailPW 는 지메일 패스워드

# e.g)   emailSend('test mail','123@gmail.com','123@naver.com','content text','image.jpg','123@gmail.com','pw123123')         #사용 예시
	print "email Send"
	msg=MIMEMultipart()
	msg['Subject']=subject
	msg['From']=sender
	msg['To']=recevier


	file=open(filename,'rb')        #이미지 파일을 연다.
	img=MIMEImage(file.read())      #이미지 파일을 읽어온다.
	file.close()  #이미지 파일을 닫는다.
	msg.attach(img)          #이미지 파일을 메일데이터에 추가한다.

	txt=MIMEText(text)
	msg.attach(txt)


	s=smtplib.SMTP('smtp.gmail.com',587)       #smtp서버 주소와 포트를 설정한다.
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login(gmailID,gmailPW)    #smtp서버에 로그인하고
	s.sendmail(gmailID,[recevier],msg.as_string())       #세팅한 메일데이터를 쏜다.
	s.quit()        #메일 전송 종료


def doorLockInput():         #키패드 입력값 확인 함수
#print "doorLock Input"
	global rows
	global cols


	matrix=[[1,2,3],              #어떤 버튼인지 확인하기 위한 매트릭스
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
					return matrix[i][j]                     #키패드값 리턴
			gpio.output(cols[j],True)


		return None
	except KeyboardInterrupt:
		gpio.cleanup()
		exit()


def handleCheck():          #핸들돌아갔는지 확인하는 함수
	return gpio.input(handleCheckPinIn)          #암컷핀에 입력값이 들어왔는지 안들어왔는지를 리턴

def main():        # 메인함수 전체적인 메인루프가 돌아가는곳

	global doorLockPW

	doorLockPW=map(int,raw_input().split(' '))      #도어락의 비밀번호를 세팅
	id=raw_input("Your Gmail ID:")                #smtp서버에 접속하기 위한 gmail 아이디 입력
	pw=raw_input("Your Gmail PW:")      #smtp에 접속하기 위한 gmail패스워드 입력
	recvID=raw_input('Recv Email ID:')          #이미지 이메일을 받을 주소 입력

	try:
		inputs=[]
		allGPIOSet()       #gpio세팅 시작
		while True:
			if distanceCheck()<20:              #거리체크해서 20cm미터 미만이면 카메라 구동시작
				cameraOpen()                   #카메라 오픈
				startTime=time.localtime().tm_min        # 1분간 켜져있어야 하므로 타이머 시작
				while True:
					if time.localtime().tm_min-startTime>=1:           # 타이머 체크해서 1분 지났는지 확인
						cameraClose()             #1분 지났으면 카메라 클로즈 하고
						break                    # 다시 거리재러 돌아감
					if handleCheck():             #만약 1분이 안지나고 핸들이 돌아갔으면
						cameraCapture()        #카메라 캡쳐하고
						cameraClose()           #카메라 끄기
						emailSend('test mail title',id,recvID,'content text','image.jpg',id,pw)    #메일 전송
					data=doorLockInput()        #만약 핸들이 안돌아갔으면 키패드에 입력값이 뭐가 들어왔는지 확인함.(입력값이 아무것도 안들어오면 None출력함.)
					breakCheck=False
					time.sleep(0.01)
					if data=='*':         #만약 입력값이 *이면
						while True:
							if handleCheck(): #다시 핸들이 돌아갔는지 확인하고 아래 3줄은 위와 같은 동작을 함.
								cameraCapture()
								cameraClose()
								emailSend('test mail title',id,recvID,'content text','image.jpg',id,pw)
							data=doorLockInput()   #입력값을 받아서 비밀번호로 이용함.
							if data=='*':        #입력으로 돌어온 값이 다시 *이면 비밀번호 입력을 종료한것으로 인식함.
								if inputs==doorLockPW: #입력값으로 들어온 비밀번호가 초기 세팅한 비밀번호와 같다면
									doorOpen()        #도어락을 오픈하라고 신호를 보냄
									print "pass door open"
								else:            #만약 비밀번호가 틀렸다면
									cameraCapture()    #캡쳐들어가고
									cameraClose()     #카메라 종료
									emailSend('test mail title',id,recvID,'content text','image.jpg',id,pw)      #이메일 전송
									print "error"
								inputs=[]
								breakCheck=True
								break
							elif data!=None:      #만약 *이 아니고 None도 아니라면
								inputs.append(data)   #현재 입력된 비밀번호에 입력값을 추가함.   ()만약 1,2가 입력되어 있는 상태에서 5가 입력값으로 들어 왔다면 1,2,5가 현재 입력된 비밀번호)
							time.sleep(0.01)
					if breakCheck:
						break
	except KeyboardInterrupt:
	     gpio.cleanup()

if __name__=="__main__":
	main()     #메인루프 시작
