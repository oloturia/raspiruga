#!/usr/bin/python
#controllo raspiruga
#pin 11,10,6,5 motore 1
#pin 14,13,12,3 motore 2

import wiringpi2 as wiringpi
import time
import threading
from subprocess import call

class movement(threading.Thread):
#	accel = 10
	realspeed = 0.1
	speedwheel = 0.1
#	decremento = 0.1
	go = False
	started = False
	avanti = False
	duration = 0
	def run(self):
		while self.started:
			if self.go:
#				self.decremento = (self.realspeed-self.speedwheel)/self.accel
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
				self.duration -=1
				if self.realspeed > self.speedwheel:
					#self.realspeed -= self.decremento
					self.realspeed -= 0.01
				else:
					self.realspeed = self.speedwheel
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
rw = 1.0
lw = 1.0
direction =""
denominator = 1.0
call(["sudo killall servod"],shell=True)
call(["sudo /home/pi/PiBits/ServoBlaster/user/servod"],shell=True)


while (direction !="quit"):
	for x in stepper1.motor:
		wiringpi.digitalWrite(x,0)
	for x in stepper2.motor:
		wiringpi.digitalWrite(x,0)
	direction = raw_input("action?(fd/bk/lt/rt/pu/pd/ad/quit) ")
	if direction != "ad" and direction != "fd" and direction != "bk" and direction !="lt" and direction !="rt" and direction !="quit" and direction !="pd" and direction !="pu":
		print "only fd,bk,lt,rt,quit"
		continue
	if direction != "quit":
		if direction !="ad" and direction !="pu" and direction !="pd":
			try:
				denominator = input("speed?(number, 0 exit) ")
			except NameError:
				print "only numbers"
				continue
			try:
				duration = input("duration?(steps) ")
				stepper1.duration = duration
				stepper2.duration = duration
			except NameError:
				print "only numbers"
				continue
		if direction == "fd":
			stepper1.avanti = True
			stepper2.avanti = True
			rw = lw = 1.0/denominator
		elif direction == "bk":
			stepper1.avanti = False
			stepper2.avanti = False
			rw = lw = 1.0/denominator
		elif direction == "rt":
			stepper1.avanti = True
			stepper2.avanti = False
			rw = lw = 1.0/denominator
		elif direction == "lt":
			stepper1.avanti = False
			stepper2.avanti = True
			rw = lw = 1.0/denominator
		elif direction == "pu":
			call(["echo 0=170 > /dev/servoblaster"],shell=True)
			duration = 0
		elif direction == "pd":
			call(["echo 0=190 > /dev/servoblaster"],shell=True)
			duration = 0
		elif direction == "ad":
			try:
				rw = input("right wheel interval? ")
				dir = input("right wheel direction? (0/1)")
				if dir == 1:
					stepper1.avanti = True
				elif dir == 0:
					stepper1.avanti = False
				else:
					print "0/1 only"
					continue
				lw = input("left wheel interval?  ")
				dir = input("left wheel direction?  (0/1)")
				if dir == 1:
					stepper2.avanti = True
				elif dir == 0:
					stepper2.avanti = False
				else:
					print "0/1 only"
					continue
				duration = input("steps? ")
				stepper1.duration = duration
				stepper2.duration = duration
			except NameError:
				print "numbers only"
				continue
		time.sleep (0.5)
		stepper1.ix = 0
		stepper2.ix = 0
		stepper1.px = 0
		stepper2.px = 0
		stepper1.speedwheel = rw
		stepper2.speedwheel = lw
		stepper1.go = True
		stepper2.go = True
		#time.sleep(duration)
		while True:
			if (stepper1.duration <= 0):
				stepper1.go = False
				stepper2.go = False
				break
	else:
		print "exit"
		call(["sudo killall servod"],shell=True)
		stepper1.started = False
		stepper2.started = False
