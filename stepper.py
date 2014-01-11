#!/bin/python
#pin 11,10,6,5 motore 1
#pin 14,13,12,3 motore 2

import wiringpi2 as wiringpi
import time
import threading
from subprocess import call

class movement(threading.Thread):
	accel = 10
	realspeed = 0.1
	decremento = 0.1
	go = False
	started = False
	avanti = False
	def run(self):
		while self.started:
			if self.go:
				self.decremento = (self.realspeed-speed)/self.accel
				wiringpi.digitalWrite(self.motor[self.ix],1)
				self.px = self.ix
				if self.avanti:
					self.ix +=1
				else:
					self.ix -=1
				if (self.ix == 4):
					self.ix = 0
				if (self.ix == -1):
					self.ix = 3
				time.sleep(self.realspeed)
				wiringpi.digitalWrite(self.motor[self.ix],1)
				time.sleep(self.realspeed)
				wiringpi.digitalWrite(self.motor[self.px],0)
				if self.realspeed > speed:
					self.realspeed -= self.decremento
				else:
					self.realspeed = speed
			else:
				for x in self.motor:
					wiringpi.digitalWrite(x,0)
				self.realspeed = 0.1


wiringpi.wiringPiSetup()
wiringpi.pinMode(11,1)
wiringpi.pinMode(10,1)
wiringpi.pinMode(6,1)
wiringpi.pinMode(5,1)
wiringpi.pinMode(14,1)
wiringpi.pinMode(13,1)
wiringpi.pinMode(12,1)
wiringpi.pinMode(3,1)

stepper1 = movement()
stepper2 = movement()

stepper1.motor = [10,11,6,5]
stepper2.motor = [14,13,12,3]
stepper1.go = False
stepper2.go = False
stepper1.started = True
stepper2.started = True
stepper1.start()
stepper2.start()
direction =""
denominator = 1.0
call(["sudo killall servod"],shell=True)
call(["sudo ./servod"],shell=True)


while (direction !="quit"):
	for x in stepper1.motor:
		wiringpi.digitalWrite(x,0)
	for x in stepper2.motor:
		wiringpi.digitalWrite(x,0)
	direction = raw_input("action?(fd/bk/lt/rt/pu/pd/quit) ")
	if direction != "fd" and direction != "bk" and direction !="lt" and direction !="rt" and direction !="pu" and direction !="pd" and direction !="quit":
		print "only fd,bk,lt,rt,pu,pd,quit"
		continue
	if direction != "quit":
		if direction != "pu" and direction !="pd":
			try:
				denominator = input("speed?(number, 0 exit) ")
			except NameError:
				print "only numbers"
				continue
			try:
				duration = input("duration?(seconds) ")
			except NameError:
				print "only numbers"
				continue
		if direction == "bk":
			stepper1.avanti = True
			stepper2.avanti = True
		elif direction == "fd":
			stepper1.avanti = False
			stepper2.avanti = False
		elif direction == "lt":
			stepper1.avanti = True
			stepper2.avanti = False
		elif direction == "rt":
			stepper1.avanti = False
			stepper2.avanti = True
		elif direction == "pu":
			call(["echo 0=90 > /dev/servoblaster"],shell=True)
			duration = 0
		elif direction == "pd":
			call(["echo 0=160 > /dev/servoblaster"],shell=True)
			duration = 0
		speed = 1.0/denominator
		time.sleep (0.5)
		stepper1.ix = 0
		stepper2.ix = 0
		stepper1.px = 0
		stepper2.px = 0
		stepper1.go = True
		stepper2.go = True
		time.sleep(duration)
		stepper1.go = False
		stepper2.go = False
	else:
		print "exit"
		call(["sudo killall servod"],shell=True)
		stepper1.started = False
		stepper2.started = False
