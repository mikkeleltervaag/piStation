import random
from decimal import *
import datetime

#My own
from settings import *

try:
	import dht11
	import glob
except:
	pass

try:
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

#Testsensor
def testSensor():
	return float(random.randint(-100, 200)/10)

class sensor:

	def __init__(self, model, hoursStored):
		self.dataTimes = []
		self.dataPoints = []
		self.hoursStored = hoursStored
		self.model = model 

	def addData(self):
		#try:
		if self.model == "DS18B20":
			dataPoint = read_temp()
		elif self.model == "testSensor":
			dataPoint = testSensor()

		self.dataPoints.append(Decimal(dataPoint))
		self.dataTimes.append(datetime.datetime.now())
		while datetime.datetime.now() - datetime.timedelta(hours=self.hoursStored) > min(self.dataTimes):
			del self.dataTimes[0]
			del self.dataPoints[0]
		#except:
		#	print "Cannot add data to datalogger"

	def getLastData(self):
		try:
			return str(self.dataPoints[-1])
		except:
			print "getLastData: No data in list"
		else:
			return "none"

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