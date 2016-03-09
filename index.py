import pygame
import time
import datetime
from time import gmtime, strftime
from random import randint
from decimal import *

#Import all settings
from settings import *
from sensor import sensor

try:
	import RPi.GPIO as GPIO
	import os
except:
	pass

# Create objects
#indoorTemperature = sensor("DS18B20", 24)
indoorTemperature = sensor("dht22_temp", 24)
indoorHumidity = sensor("dht22_hum", 24)
#indoorTemperature = sensor("testSensor", 24)
	
while True:

	# Clear screen
	screen.fill(black)

	# Add to datalogger
	indoorTemperature.addData()

	# Draw Graph
	#indoorTemperature.drawGraph(10,70,1660,970, size=3, color=green, hSeperator="hour", vSeperator=1, smooth=5)
	indoorTemperature.drawGraph(10,70,1660,480, size=3, color=green, hSeperator="hour", vSeperator=1, smooth=5)
	indoorHumidity.drawGraph(10,560,1660,480, size=3, color=blue, hSeperator="hour", vSeperator=1, smooth=5)

	# Top of screen
	screen.blit(topText.render(str(indoorTemperature.getLastData())+unichr(176).encode("latin-1")+"C", True, white), (10, 0))
	screen.blit(topText.render(str(indoorHumidity.getLastData())+"%", True, white), (300, 0))
	screen.blit(topText.render(strftime("%H:%M", time.localtime()), True, white), (screenWidth-185, 0))
	
	#Update screen
	pygame.display.update()

	#Sleep
	time.sleep(61-datetime.datetime.now().second)
	#time.sleep(1)