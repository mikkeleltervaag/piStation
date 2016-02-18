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