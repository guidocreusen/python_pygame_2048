#imports
import pygame
from pygame.locals import *
import sys

#init
pygame.init()
screen = pygame.display.set_mode((640, 640), 0, 32)

#main loop
while True:

	#wait for event
	event = pygame.event.wait()
	if event.type == QUIT:
		sys.exit()

	#draw bg
	screen.fill((200,200,200))

	pygame.display.update()