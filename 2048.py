#imports
import pygame
from pygame.locals import *
import sys

from board import Board

#constants
SCR_SIZE = (640, 640)
MARGINS = (100, 100)

#init
pygame.init()
scr = pygame.display.set_mode(SCR_SIZE, 0, 32)
scr.fill((240,240,240))

board = Board()
board.add_random_square()

board.draw(scr, SCR_SIZE, MARGINS)

pygame.display.update()

#main loop
while True:

	#wait for event
	event = pygame.event.wait()
	if event.type == QUIT:
		sys.exit()
	elif event.type == KEYDOWN:
		if event.key ==  K_LEFT:
			board.move_in_direction("left")
		elif event.key ==  K_RIGHT:
			board.move_in_direction("right")
		elif event.key ==  K_UP:
			board.move_in_direction("up")
		elif event.key ==  K_DOWN:
			board.move_in_direction("down")
	else:
		continue

	board.add_random_square()

	#draw bg
	scr.fill((240,240,240))

	#draw board
	board.draw(scr, SCR_SIZE, MARGINS)

	pygame.display.update()