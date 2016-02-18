import pygame
import time
import datetime
from time import gmtime, strftime
from random import randint
from decimal import *

try:
	import RPi.GPIO as GPIO
	import dht11
	import os
	import glob

	# DHT11
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.cleanup()
	instance = dht11.DHT11(pin = 4)
	GPIO.setup(10, GPIO.IN)

	#DS18B20
	os.system('modprobe w1-gpio')
	os.system('modprobe w1-therm')
	base_dir = '/sys/bus/w1/devices/'
	device_folder = glob.glob(base_dir + '28*')[0]
	device_file = device_folder + '/w1_slave'
	
except:
	pass

#DS18B20
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return "%.1f" % temp_c


# Variables
screenWidth = 1680
screenHeight = 1050

# Init pygame
screen = pygame.display.set_mode((screenWidth,screenHeight), pygame.FULLSCREEN)
pygame.init()
pygame.mouse.set_visible(False)

# Fonts
debugText = pygame.font.SysFont("monospace", 12)
topText = pygame.font.SysFont("monospace", 60)

# Colors
black = (0,0,0)
white = (255,255,255)
gray = (100,100,100)
blue = (0,0,255)
green = (0,255,0)

class sensor:

	def __init__(self, hoursStored):
		self.dataTimes = []
		self.dataPoints = []
		self.hoursStored = hoursStored

	def addData(self, dataTime, dataPoint):
		self.dataTimes.append(dataTime)
		self.dataPoints.append(Decimal(dataPoint))
		while datetime.datetime.now() - datetime.timedelta(hours=self.hoursStored) > min(self.dataTimes):
			del self.dataTimes[0]
			del self.dataPoints[0]

	def getLastData(self):
		try:
			return self.dataPoints[-1]
		except:
			print "getLastData: No data in list"

	def drawGraph(self, startX, startY, width, height, size=1, color=white, background=False, border=white, bordersize=1, hSeperator=False, vSeperator=False, gridColor=gray, girdSize=1):

		if background != False:
			pygame.draw.rect(screen, (background), (startX, startY, width, height), 0)
		if border != False:
			pygame.draw.rect(screen, (border), (startX, startY, width, height), bordersize)

		if len(self.dataPoints) < 2 or max(self.dataPoints) == min(self.dataPoints):
			screen.blit(debugText.render('Too few data points!', True, color), (startX, startY))
		else:
			dataHeight = Decimal(height)/Decimal((max(self.dataPoints)-min(self.dataPoints)))
			dataWidth = Decimal(width)/Decimal((max(self.dataTimes)-min(self.dataTimes)).seconds)

			if hSeperator == "hour":
				firstHour = (60-min(self.dataTimes).minute)*60+(60-min(self.dataTimes).second)
				for x in xrange(0,int(((max(self.dataTimes)-min(self.dataTimes)).seconds)),3600):
					pygame.draw.line(screen, gridColor, (startX+((x+firstHour)*dataWidth),startY), (startX+((x+firstHour)*dataWidth),startY+height), girdSize)

			if vSeperator != False:
				for y in xrange(int(min(self.dataPoints)),int(max(self.dataPoints)), vSeperator):
					yIn = startY+height-(dataHeight*(y-min(self.dataPoints)))
					if startY+height != yIn:
						pygame.draw.line(screen, gridColor, (startX,yIn), (startX+width,yIn), girdSize)
						screen.blit(debugText.render(str(y)+unichr(176).encode("latin-1")+"C", True, color), (startX+width+5, yIn-5))

			for dataPoint in range(2, len(self.dataPoints)):
				x1 = startX+((self.dataTimes[dataPoint-2]-min(self.dataTimes)).seconds*dataWidth)
				y1 = startY+height-(dataHeight*(self.dataPoints[dataPoint-1]-min(self.dataPoints)))
				x2 = startX+((self.dataTimes[dataPoint-1]-min(self.dataTimes)).seconds*dataWidth)
				y2 = startY+height-(dataHeight*(self.dataPoints[dataPoint]-min(self.dataPoints)))
				pygame.draw.line(screen, color, (x1,y1), (x2,y2), size)

indoorTemperature = sensor(24)
	
while True:

	# Clear screen
	screen.fill(black)

	# Add to datalogger
	try:
		indoorTemperature.addData(datetime.datetime.now(),read_temp())
	except:
		print "Cannot add data to datalogger"

	# Draw Graph
	indoorTemperature.drawGraph(10,90,1660,950, size=3, color=green, hSeperator="hour", vSeperator=1)

	# Top of screen
	screen.blit(topText.render(str(indoorTemperature.getLastData())+unichr(176).encode("latin-1")+"C", True, white), (10, 0))
	screen.blit(topText.render(strftime("%H:%M", time.localtime()), True, white), (screenWidth-185, 0))
	
	#Update screen
	pygame.display.update()
	
	#Sleep
	time.sleep(61-datetime.datetime.now().second)