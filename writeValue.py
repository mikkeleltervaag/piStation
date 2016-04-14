# My imports
from settings import *

def writeValue(tileX, tileY, tileWidth, tileHeight, sensor, extraText=""):

	x = (tileX*tileSize)+((tileSpaceing+1)*(tileX+1))
	y = (tileY*tileSize)+((tileSpaceing+1)*(tileY+1))
	width = tileWidth*tileSize+(tileSpaceing*(tileWidth-1))
	height = tileHeight*tileSize+(tileSpaceing*(tileHeight-1))

	pygame.draw.rect(screen, tileColor, (x, y, width, height), 0)

	value = str(sensor.dataPoints[-1])

	try:
		if sensor.dataPoints[-1] > sensor.dataPoints[-2]:
			color = green
		elif sensor.dataPoints[-1] < sensor.dataPoints[-2]:
			color = red
		else:
			color = white
	except:
		print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " Cant get color from model " + str(sensor.model)
		color = white


	sizeCheckX = -1
	sizeCheckY = -1
	i = 0
	while sizeCheckY < 0 or sizeCheckX < 0:

		valueFont = pygame.font.SysFont(font, (70*tileWidth)-(i*10))
		valueText = valueFont.render(str(sensor.dataPoints[-1]), True, color)

		dateFont = pygame.font.SysFont(font, (20*tileWidth)-(i))
		dateText = dateFont.render(sensor.dataTimes[-1].strftime("%H:%M"), True, gray)

		sizeCheckY = (tileSize*tileHeight)-valueText.get_height()-dateText.get_height()-tileSpaceing
		sizeCheckX = (tileSize*tileWidth)-valueText.get_width()-tileSpaceing
		i = i + 1

	startDrawingY = y+(((tileSize*tileHeight)-valueText.get_height()-dateText.get_height())/2)

	screen.blit(valueText, (x + ((width-valueText.get_width())/2), startDrawingY))
	screen.blit(dateText, (x + ((width-dateText.get_width())/2), startDrawingY+valueText.get_height()))


	pygame.display.update()

