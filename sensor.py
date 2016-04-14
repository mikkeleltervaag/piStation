# My imports
from settings import *
from brentCrude import *

class sensor:

	def __init__(self, model, fileName, hoursStored):
		self.dataTimes = []
		self.dataPoints = []
		self.model = model
		self.fileName = fileName
		self.hoursStored = hoursStored
		self.lastStoredData = datetime.datetime.now()
		self.lastData = None

	def readData(self):
		if self.model == "test":
			self.lastData = float(random.randint(220, 250))/10
		elif self.model == "brentCrude":
			self.lastData = float(getBrentCrude())
		else:
			#try:
			bluetoothSerial = serial.Serial( "/dev/rfcomm1", baudrate=9600 )
			bluetoothSerial.write(str(self.model))
			self.lastData = float(bluetoothSerial.readline().rstrip('\n\r'))
			#except:
			#	print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " Serial error with model " + str(self.model)

	def addData(self):
		
		if self.lastData != "none":
			self.dataPoints.append(self.lastData)
			self.dataTimes.append(datetime.datetime.now())
		
		try:
			if  self.dataPoints[-1] == self.dataPoints[-2]:
				del self.dataTimes[-1]
				del self.dataPoints[-1]
		except:
			print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " Cannot delete copy in model " + str(self.model)


		try:
			while datetime.datetime.now() - datetime.timedelta(hours=self.hoursStored) > min(self.dataTimes):
				del self.dataTimes[0]
				del self.dataPoints[0]
		except:
			print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " Cannot delete data in model " + str(self.model)

	def storeData(self):

		tempDataTimes = [datetime.datetime.now()]
		tempDataPoints = [0]
		i = 0
		while self.lastStoredData < tempDataTimes[-1] and i < len(self.dataTimes):
			i = i + 1
			tempDataTimes.append(self.dataTimes[-i])
			tempDataPoints.append(self.dataPoints[-i])

		if len(tempDataTimes) > 2:

			del tempDataPoints[0]
			del tempDataPoints[-1]

			allPoints = 0
			for i in range(0, len(tempDataPoints)):
				allPoints = allPoints + tempDataPoints[i]

			try:
				with open(self.fileName, 'ab') as fp:
					saveCSV = csv.writer(fp)
					saveCSV.writerow([datetime.datetime.now()] + [allPoints/len(tempDataPoints)])
			except:
				print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " Cannot store data with model " + str(self.model)

			self.lastStoredData = datetime.datetime.now()
			
	def importData(self):
		try:
			with open(self.fileName, 'rb') as f:
			    reader = csv.reader(f)
			    for row in reader:
			    	if datetime.datetime.now() - datetime.timedelta(hours=self.hoursStored) < datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f"):
			    		self.dataPoints.append(decimal.Decimal(row[1]))
			    		self.dataTimes.append(datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f"))
		except:
			print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " Cannot get data from CSV " + str(self.model)