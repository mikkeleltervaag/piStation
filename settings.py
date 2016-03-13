import pygame

# Variables
screenWidth = 1680
screenHeight = 1050

# Init pygame
screen = pygame.display.set_mode((screenWidth,screenHeight), pygame.FULLSCREEN)
pygame.init()
pygame.mouse.set_visible(False)

# Fonts
debugText = pygame.font.SysFont("monospace", 16)
topText = pygame.font.SysFont("monospace", 60)

# Colors
black = (0,0,0)
white = (255,255,255)
gray = (100,100,100)
darkGray = (30,30,30)
blue = (0,0,255)
green = (0,255,0)