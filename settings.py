import pygame
import time
import datetime
import random
import csv
import decimal
import urllib

try:
	import RPi.GPIO as GPIO
	import os
except:
	print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " Cannot import Raspberry pi"

# Screen size
screenWidth = 1680
screenHeight = 1050

# Tile size
tileSize = 240
tileSpaceing = 16

# Init pygame
screen = pygame.display.set_mode((screenWidth,screenHeight), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.init()
pygame.mouse.set_visible(False)

# Font
font = "Verdana"

# Colors
tileColor = (50,50,50)

black = (0,0,0)
white = (255,255,255)
gray = (100,100,100)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)

# Error meassages
error = []