import pygame
import time
from datetime import datetime, timedelta
from time import gmtime, strftime
import random
from decimal import *


#Import all settings
from settings import *
from sensor import sensor

try:
	import RPi.GPIO as GPIO
	import os

	# GPIO Human detector
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17, GPIO.IN)

except:
	pass

thisMinute = datetime.now().minute - 1
thisHour = datetime.now().hour - 1

motionDetected = 0


# Create objects
#indoorTemperature = sensor("DS18B20", 24)
indoorTemperature = sensor("dht22_temp", 24)
outdoorTemperature = sensor(100, 24)
bedroomTemperature = sensor(101, 24)
indoorHumidity = sensor("dht22_hum", 24)
humanDetector = sensor("pir", 24)
#indoorTemperature = sensor("testSensor", 24)

indoorTemperature.importData('indoorTemperature.csv')
	
while True:

	if datetime.now().minute == thisMinute + 1:
		thisMinute = datetime.now().minute
		everyMinute = True
	else:
		everyMinute = False

	if datetime.now().hour == thisHour + 1:
		thisHour = datetime.now().hour
		everyHour = True
	else:
		everyHour = False

	try:
		if GPIO.input(17):
			motionDetected = motionDetected + 1
	except:
		pass
	

	if everyMinute:
		# Clear screen
		screen.fill(black)

		# Add to datalogger
		indoorTemperature.addData()
		outdoorTemperature.addData()
		bedroomTemperature.addData()
		indoorHumidity.addData()
		humanDetector.addData()

		# Reset motion detection
		motionDetected = 0

		# Draw Graph
		#indoorTemperature.drawGraph(10,70,1660,970, size=3, color=green, hSeperator="hour", vSeperator=1, smooth=5)
		humanDetector.drawGraph(10,70,1660,480, size=20, color=darkGray, border=False, smooth=10)
		bedroomTemperature.drawGraph(10,70,1660,480, size=3, color=blue, border=False, shared=indoorTemperature.dataPoints)
		indoorTemperature.drawGraph(10,70,1660,480, size=3, color=green, hSeperator="hour", vSeperator=1, shared=bedroomTemperature.dataPoints)
		outdoorTemperature.drawGraph(10,560,825,480, size=3, color=green, hSeperator="hour", vSeperator=1)
		indoorHumidity.drawGraph(850,560,825,480, size=3, color=blue, hSeperator="hour", vSeperator=1)

		# Top of screen
		topInfo = str(indoorTemperature.getLastData())+unichr(176).encode("latin-1")+"C "
		topInfo = topInfo + "(B:"+str(bedroomTemperature.getLastData())+unichr(176).encode("latin-1")+"C "
		topInfo = topInfo + "O:"+str(outdoorTemperature.getLastData())+unichr(176).encode("latin-1")+"C) "
		topInfo = topInfo + str(indoorHumidity.getLastData())+"%"
		#screen.blit(topText.render(str(motionDetected), True, white), (600, 0))
		screen.blit(topText.render(strftime("%H:%M", time.localtime()), True, white), (screenWidth-185, 0))

		screen.blit(topText.render(topInfo, True, white), (10, 0))
		
		#Update screen
		pygame.display.update()

	#if everyHour:
		indoorTemperature.storeData('indoorTemperature.csv')

	#Sleep
	#time.sleep(61-datetime.datetime.now().second)
	time.sleep(1)