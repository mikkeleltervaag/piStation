import random
from decimal import *
import datetime
import math
import time
import csv



#My own
from settings import *

try:
	import serial
	bluetoothSerial = serial.Serial( "/dev/rfcomm1", baudrate=9600 )
	import RPi.GPIO as GPIO
	import os
	import glob
	import Adafruit_DHT
except:
	print "import error"

try:
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
        return temp_c

#Testsensor
def testSensor():
	return float(random.randint(220, 250))/10

#Motion sensor
def pir():
	from index import motionDetected
	return motionDetected

def blueTooth(num):
	bluetoothSerial.write(str(num))
	test = float(bluetoothSerial.readline().rstrip('\n\r'))
	print test
	return test
 
class sensor:

	def __init__(self, model, hoursStored):
		self.dataTimes = []
		self.dataPoints = []
		self.hoursStored = hoursStored
		self.model = model 

	def addData(self):
		try:
			if self.model == "DS18B20":
				dataPoint = read_temp()
			elif self.model == "testSensor":
				dataPoint = testSensor()
			elif self.model == "pir":
				dataPoint = pir()
			elif self.model == "dht22_temp":
				humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
				dataPoint = temperature
			elif self.model == "dht22_hum":
				humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
				dataPoint = humidity
			elif self.model == 100:
				dataPoint = blueTooth(100)
			elif self.model == 101:
				dataPoint = blueTooth(101)

			self.dataPoints.append(Decimal(dataPoint))
			self.dataTimes.append(datetime.datetime.now())
			while datetime.datetime.now() - datetime.timedelta(hours=self.hoursStored) > min(self.dataTimes):
				del self.dataTimes[0]
				del self.dataPoints[0]
		except:
			print "Cannot add data to datalogger"

	def storeData(self, name):
		with open(name, 'ab') as fp:
			indoorTemperatureCSV = csv.writer(fp)
			indoorTemperatureCSV.writerow([self.dataTimes] + [self.dataPoints[-1]])

	def importData(self, name):
		try:
			with open(name, 'rb') as f:
			    reader = csv.reader(f)
			    for row in reader:
			    	if datetime.datetime.now() - datetime.timedelta(hours=self.hoursStored) < row[0]:
			    		self.dataPoints.append(row[1])
			    		self.dataTimes.append(row[0])
		except:
			pass

	def getLastData(self):
		try:
			return str("%.1f" % self.dataPoints[-1])
		except:
			print "getLastData: No data in list"
		else:
			return "none"

	def drawGraph(self, startX, startY, width, height, size=1, color=white, background=False, border=white, bordersize=1, hSeperator=False, vSeperator=False, gridColor=gray, girdSize=1, smooth=False, shared=False):

		if background != False:
			pygame.draw.rect(screen, (background), (startX, startY, width, height), 0)
		if border != False:
			pygame.draw.rect(screen, (border), (startX, startY, width, height), bordersize)

		if smooth:
			minimumListItems = smooth+2
		else:
			minimumListItems = 2

		if len(self.dataPoints) < minimumListItems or max(self.dataPoints) ==  min(self.dataPoints):
			screen.blit(debugText.render('Too few data points!', True, color), (startX+5, startY+5))
		else:
			dataMinimum = min(self.dataPoints)-((max(self.dataPoints)-min(self.dataPoints))*Decimal(0.1))
			dataMaximum = max(self.dataPoints)+((max(self.dataPoints)-min(self.dataPoints))*Decimal(0.1))

			if shared != False and len(shared) > 1:


				checkDataMinimum = min(shared)-((max(shared)-min(shared))*Decimal(0.1))
				checkDataMaximum = max(shared)+((max(shared)-min(shared))*Decimal(0.1))

				if checkDataMinimum < dataMinimum and checkDataMinimum != 0:
					dataMinimum = checkDataMinimum
				if checkDataMaximum > dataMaximum:
					dataMaximum = checkDataMaximum





			timeMaximum = max(self.dataTimes)
			timeMinimum = self.dataTimes[0]

			dataHeight = Decimal(height)/Decimal((dataMaximum-dataMinimum))
			dataWidth = Decimal(width)/Decimal((max(self.dataTimes)-timeMinimum).seconds)

			if hSeperator == "hour":
				firstHour = (60-timeMinimum.minute)*60+(60-timeMinimum.second)
				for x in xrange(0,int(((timeMaximum-timeMinimum).seconds)),3600):
					pygame.draw.line(screen, gridColor, (startX+((x+firstHour)*dataWidth),startY), (startX+((x+firstHour)*dataWidth),startY+height), girdSize)

			if vSeperator != False:
				for y in xrange(int(math.ceil(dataMinimum)),int(math.ceil(dataMaximum)), vSeperator):
					yIn = startY+height-(dataHeight*(y-dataMinimum))
					if startY+height != yIn:
						pygame.draw.line(screen, gridColor, (startX,yIn), (startX+width,yIn), girdSize)
					if startY+height-30 > yIn:
						if self.model == "DS18B20":
							screen.blit(debugText.render(str(y)+unichr(176).encode("latin-1")+"C", True, color), (startX+width-50, yIn+5))
						elif self.model == "dht22_temp":
							screen.blit(debugText.render(str(y)+unichr(176).encode("latin-1")+"C", True, color), (startX+width-50, yIn+5))
						elif self.model == "dht22_hum":
							screen.blit(debugText.render(str(y)+"%", True, color), (startX+width-50, yIn+5))
						else:
							screen.blit(debugText.render(str(y), True, color), (startX+width-50, yIn+5))
			
			for dataPoint in range(2, len(self.dataPoints)):

				if smooth:
					smoothing = 0
					for x in xrange(1,smooth):
						smoothing = smoothing + self.dataPoints[dataPoint-x]
					point1 = (self.dataPoints[dataPoint-smooth]+smoothing)/smooth
					point2 = (self.dataPoints[dataPoint]+smoothing)/smooth
				else:
					point1 = self.dataPoints[dataPoint-1]
					point2 = self.dataPoints[dataPoint]

				x1 = startX+((self.dataTimes[dataPoint-2]-min(self.dataTimes)).seconds*dataWidth)
				y1 = startY+height-(dataHeight*(point1-dataMinimum))
				x2 = startX+((self.dataTimes[dataPoint-1]-min(self.dataTimes)).seconds*dataWidth)
				y2 = startY+height-(dataHeight*(point2-dataMinimum))
				pygame.draw.line(screen, color, (x1,y1), (x2,y2), size)