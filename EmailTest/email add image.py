# -*- coding: utf-8 -*-
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

msg=MIMEMultipart()
msg['Subject']='안녕'
msg['From']='123@gmail.com'
msg['To']='123@naver.com'


file=open('qwe123.jpg','rb')
img=MIMEImage(file.read())
file.close()
msg.attach(img)

txt=MIMEText('안녕 반가워요')
msg.attach(txt)


s=smtplib.SMTP('smtp.gmail.com',587)
s.ehlo()
s.starttls()
s.ehlo()
s.login('123@gmail.com','123456!')
s.sendmail('123@gmail.com',['123@naver.com'],msg.as_string())
s.quit()
