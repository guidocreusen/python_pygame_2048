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
			if board.move_in_direction("left"):
				board.add_random_square()
		elif event.key ==  K_RIGHT:
			if board.move_in_direction("right"):
				board.add_random_square()
		elif event.key ==  K_UP:
			if board.move_in_direction("up"):
				board.add_random_square()
		elif event.key ==  K_DOWN:
			if board.move_in_direction("down"):
				board.add_random_square()
	else:
		continue

	#draw bg
	scr.fill((240,240,240))

	#draw board
	board.draw(scr, SCR_SIZE, MARGINS)

	pygame.display.update()