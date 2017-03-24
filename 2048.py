#imports
import pygame
from pygame.locals import *
import sys

from board import Board

#constants
SCREEN_SIZE = (640, 640)
MARGINS = 80

#init
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
board = Board()

#main loop
while True:

	#wait for event
	event = pygame.event.wait()
	if event.type == QUIT:
		sys.exit()

	#draw bg
	screen.fill((240,240,240))

	#draw board
	screen.blit(board.draw_bg(SCREEN_SIZE[0]-2*MARGINS), (MARGINS,MARGINS))

	pygame.display.update()