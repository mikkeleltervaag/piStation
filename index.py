# My imports
from settings import *
from clockTile import *
from sensor import *
from writeValue import *
from brentCrude import *

# Setup all sensores
outdoorTemperature = sensor(100, "outdoorTemperature.csv", 24)
bedroomTemperature = sensor(101, "bedroomTemperature.csv", 24)
brentCrudeTicker = sensor("brentCrude", "brentCrude.csv", 24)

# Import data from sensors
outdoorTemperature.importData()
bedroomTemperature.importData()
brentCrudeTicker.importData()

# Variables for the time
thisMinute = datetime.datetime.now()
thisTenMinute = datetime.datetime.now()
thisHour = datetime.datetime.now()


while True:

	# Every Minute
	if datetime.datetime.now() >= thisMinute:
		thisMinute = datetime.datetime.now() + datetime.timedelta(minutes=1)

		# Read Sensor data
		outdoorTemperature.readData()
		bedroomTemperature.readData()
		brentCrudeTicker.readData()

		# Add sensor data
		outdoorTemperature.addData()
		bedroomTemperature.addData()
		brentCrudeTicker.addData()

		# Tiles
		clock(0, 0, 2, 1)
		writeValue(0, 1, 1, 1, bedroomTemperature, unichr(176).encode("latin-1")+"C")
		writeValue(1, 1, 1, 1, outdoorTemperature, unichr(176).encode("latin-1")+"C")
		writeValue(6, 0, 2, 1, brentCrudeTicker)

		print "0"

		
	# Every Ten Minute
	if datetime.datetime.now() >= thisTenMinute:
		thisTenMinute = datetime.datetime.now() + datetime.timedelta(minutes=10)
		
		# Store sensor data
		bedroomTemperature.storeData()
		outdoorTemperature.storeData()
		brentCrudeTicker.storeData()

		print "1"

		

	# Sleep to next minute
	print time.strftime("%H:%M:%S", time.localtime())
	time.sleep(60-datetime.datetime.now().second)
	#time.sleep(1)
