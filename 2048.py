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
key_bindings = {
	K_LEFT: "left",
	K_RIGHT: "right",
	K_UP: "up",
	K_DOWN: "down"
}

board.draw(scr, SCR_SIZE, MARGINS)

pygame.display.update()

#main loop
while True:

	#wait for event until either quit or keypress
	event = pygame.event.wait()
	valid_move = False
	if event.type == QUIT:
		sys.exit()
	elif event.type == KEYDOWN:
		#if a valid move is made add a square
		if event.key in key_bindings:
			if board.move_in_direction(key_bindings[event.key]):
				board.add_random_square()			
	else:
		continue

	#draw bg and board
	scr.fill((240,240,240))
	board.draw(scr, SCR_SIZE, MARGINS)

	pygame.display.update()