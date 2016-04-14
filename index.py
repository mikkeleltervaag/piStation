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
thisMinute = datetime.datetime.now().minute - 1
thisTenMinute = (datetime.datetime.now().minute/10) - 1
thisHour = datetime.datetime.now().hour - 1


while True:

	# Every Minute
	if datetime.datetime.now().minute == thisMinute + 1:
		thisMinute = datetime.datetime.now().minute

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
		writeValue(4, 0, 2, 1, brentCrudeTicker)

		
	# Every Ten Minute
	if (datetime.datetime.now().minute/10) == thisTenMinute + 1:
		thisTenMinute = datetime.datetime.now().minute/10
		
		# Store sensor data
		bedroomTemperature.storeData()
		outdoorTemperature.storeData()
		brentCrudeTicker.storeData()

		

	# Sleep to next minute
	time.sleep(60-datetime.datetime.now().second)
	#time.sleep(1)
