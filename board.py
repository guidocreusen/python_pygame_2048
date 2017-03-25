#imports
import pygame
from aaroundedrect import *

#board class stores square value as list of lists

class Board(object):
	#stores the squares value
	squares = []

	#stores the colors of squares
	colors = {
		0: (120, 100, 100),
		2: (240, 240, 240),
		4: (255, 0, 0),
		8: (204, 128, 51),
		16: (204, 51, 51),
		32: (204, 51, 128),
		64: (149, 189, 229)
	}

	def __init__(self, bg_col):
		#set bg color
		self.bg_col = bg_col
		#set all values to 0
		for i in range(4):
			self.squares.append([0, 0, 0, 0])

	#draws the background, blits a surface with dimensions (size, size)
	def draw_bg(self, surface, size, margins):
		bg_rect = pygame.Rect(0, 0, size[0]-2*margins[0], size[1]-2*margins[1])
		bg_rounded = AAfilledRoundedRect(bg_rect, self.bg_col, 0.04)

		return surface.blit(bg_rounded, (margins[0], margins[1]))

	#draw the squares which make up the board
	def draw_squares(self, surface, size, margins):
		#distribute space: 5 x 4% empty, 4 x 20% square
		
		#iterate over board
		#start drawing at y_margin (mult. empirical factor!) + top border width
		draw_y = (margins[1]*0.955)+size[1]*0.03
		for x_row in self.squares:
			

			#start drawing at x_margin (mult. empirical factor!) + left border width
			draw_x = (margins[0]*0.955)+size[0]*0.03
			#draw the squares
			for square in x_row:
				square_rect = pygame.Rect(0,0, 0.2125*(size[0]-2*margins[0]), 0.2125*(size[1]-2*margins[1]))
				square_rounded = AAfilledRoundedRect(square_rect, (200,200,200), 0.1)
				surface.blit(square_rounded, (draw_x, draw_y))

				draw_x += 0.2425*(size[0]-2*margins[0])

			draw_y += 0.2425*(size[1]-2*margins[1])

	#draws the entire board, by first drawing bg then squares
	def draw(self, surface, size, margins):
		self.draw_bg(surface, size, margins)
		self.draw_squares(surface, size, margins)

