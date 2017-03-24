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

	def __init__(self):
		#set all values to 0
		for i in range(4):
			self.squares.append([0, 0, 0, 0])


	#draws the background, returns a surface with dimensions (size, size)
	def draw_bg(self, size):
		bg_rect = pygame.Rect(0, 0, size, size)
		bg = AAfilledRoundedRect(bg_rect, (100,120,100), 0.05)

		return bg

		

