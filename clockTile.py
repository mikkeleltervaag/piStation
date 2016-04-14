# My imports
from settings import *

def clock(tileX, tileY, tileWidth, tileHeight):

	x = (tileX*tileSize)+((tileSpaceing+1)*(tileX+1))
	y = (tileY*tileSize)+((tileSpaceing+1)*(tileY+1))
	width = tileWidth*tileSize+(tileSpaceing*(tileWidth-1))
	height = tileHeight*tileSize+(tileSpaceing*(tileHeight-1))

	pygame.draw.rect(screen, tileColor, (x, y, width, height), 0)

	sizeCheckX = -1
	sizeCheckY = -1
	i = 0
	while sizeCheckY < 0 and sizeCheckX < 0:

		clockFont = pygame.font.SysFont(font, (70*tileWidth)-(i*10))
		clockText = clockFont.render(time.strftime("%H:%M", time.localtime()), True, white)

		dateFont = pygame.font.SysFont(font, 30*(tileWidth-i))
		dateText = dateFont.render(time.strftime("%Y-%m-%d", time.localtime()), True, white)

		sizeCheckY = (tileSize*tileHeight)-clockText.get_height()-dateText.get_height()-(tileSpaceing*3)
		sizeCheckX = (tileSize*tileWidth)-clockText.get_width()-tileSpaceing
		i = i + 1

	startDrawingY = y+(((tileSize*tileHeight)-clockText.get_height()-dateText.get_height())/2)

	screen.blit(clockText, (x + ((width-clockText.get_width())/2), startDrawingY))
	screen.blit(dateText, (x + ((width-dateText.get_width())/2), startDrawingY+clockText.get_height()))

	pygame.display.update()

