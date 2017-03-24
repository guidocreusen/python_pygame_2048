#imports
import pygame
from pygame.locals import *
import sys

from board import Board

#constants
SCR_SIZE = (640, 640)
MARGINS = (80, 80)

#init
pygame.init()
scr = pygame.display.set_mode(SCR_SIZE, 0, 32)
board = Board((160, 160, 170))

#main loop
while True:

	#wait for event
	event = pygame.event.wait()
	if event.type == QUIT:
		sys.exit()

	#draw bg
	scr.fill((240,240,240))

	#draw board
	board.draw_bg(scr, SCR_SIZE, MARGINS)

	pygame.display.update()