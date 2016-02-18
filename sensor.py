import pygame
import time
import datetime
from time import gmtime, strftime
from random import randint
from decimal import *

from settings import *

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