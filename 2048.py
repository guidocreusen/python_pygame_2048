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
board.add_square(2, (0,0))
board.add_square(4, (2,0))
board.add_square(2, (3,0))

board.add_square(2, (2,1))
board.add_square(2, (3,1))

board.add_square(4, (0,2))
board.add_square(2, (2,2))
board.add_square(2, (3,2))

board.add_square(4, (0,3))
board.add_square(4, (1,3))
board.add_square(4, (2,3))
board.add_square(4, (3,3))

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
	else:
		continue

	#draw bg
	scr.fill((240,240,240))

	#draw board
	board.draw(scr, SCR_SIZE, MARGINS)

	pygame.display.update()