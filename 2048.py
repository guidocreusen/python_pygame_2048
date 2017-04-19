#imports
import pygame
from pygame.locals import *
import sys
from aaroundedrect import *
from board import Board

#constants
SCR_SIZE = (640, 640)
MARGINS = (100, 100)

#init
pygame.init()
scr = pygame.display.set_mode(SCR_SIZE, 0, 32)
scr.fill((240,240,240))

board = Board(scr, SCR_SIZE, MARGINS)
board.add_random_square()
board.add_random_square()

key_bindings = {
	K_LEFT: "left",
	K_RIGHT: "right",
	K_UP: "up",
	K_DOWN: "down"
}

board.draw()

pygame.display.update()

#shows the game over message
def game_over():
	board.draw()
	pygame.display.update()

	#wait for a certain amount of time (in ms) before trigerring the game over overlay
	wait_time = 1000
	animation_time = 2000
	framerate = 200
	time_elapsed = 0
	pygame.time.delay(wait_time)
	clock = pygame.time.Clock()

	#animation loop
	while time_elapsed < animation_time:
		dt = clock.tick(framerate)
		animation_progress = time_elapsed/animation_time

		#draw the transparent background overlay, fade to white with alpha 200
		board.draw()
		overlay = pygame.Surface((SCR_SIZE[0], SCR_SIZE[1]), pygame.SRCALPHA)
		overlay.fill((255,255,255, 200*animation_progress))
		scr.blit(overlay, (0,0))

		pygame.display.update()
		time_elapsed += dt
	
	#rounded rect holding game over text
	game_over_rect = pygame.Rect(0,0, 300, 150)
	game_over_rect_rounded = AAfilledRoundedRect(game_over_rect, (200,200,200), 0.2)
	scr.blit(game_over_rect_rounded, (SCR_SIZE[0]/2-150,SCR_SIZE[1]/2-75))
	#game over text message
	font = pygame.font.SysFont("bold", 60)
	font_small = pygame.font.SysFont("arial", 15)
	txt_game_over = font.render("Game Over", True, (50,50,50))
	txt_press_button = font_small.render("press any key to exit", True, (50,50,50))
	scr.blit(txt_game_over, (SCR_SIZE[0]/2-txt_game_over.get_width()/2,SCR_SIZE[1]/2-txt_game_over.get_height()/2))
	scr.blit(txt_press_button, (SCR_SIZE[0]/2-txt_press_button.get_width()/2,SCR_SIZE[1]/2-txt_game_over.get_height()/2+50))

	pygame.display.update()

	#wait for keypress or quit, then exit programm (clear event queue first)
	pygame.event.get()
	event = pygame.event.wait()
	while not (event.type == KEYDOWN or event.type == QUIT):
		event = pygame.event.wait()
		continue
	sys.exit()

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
				board.update_squares_position()		
				board.add_random_square()
	else:
		continue

	#game over
	if board.game_over():
		game_over()

	#draw bg and board
	scr.fill((240,240,240))
	board.draw()

	pygame.display.update()
