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
	def draw_bg(self, screen, scr_size, margins):
		bg_rect = pygame.Rect(0, 0, scr_size[0]-2*margins[0], scr_size[1]-2*margins[1])
		bg = AAfilledRoundedRect(bg_rect, self.bg_col, 0.05)

		return screen.blit(bg, (margins[0], margins[1]))

		

