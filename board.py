#imports
import pygame
from aaroundedrect import *

class Board(object):
	#stores the squares value
	squares = []

	#color values
	bg_color = (187, 173, 160)
	colors = {
		0: (205, 192, 180),
		2: (238, 228, 218),
		4: (237, 224, 200),
		8: (242, 177, 121),
		16: (245, 150, 99),
		32: (246, 124, 95),
		64: (246, 107, 65),
		128: (237, 208, 114),
		256: (237, 204, 97),
		512: (237, 200, 80)
	}
	txt_color_light = (249,247,243)
	txt_color_dark = (117, 109, 101)

	def __init__(self):

		#set all values to 0
		for i in range(4):
			self.squares.append([0, 2, 4, 8])

	#draws the background, blits a surface with dimensions (size, size)
	def draw_bg(self, surface, size, margins):
		bg_rect = pygame.Rect(0, 0, size[0]-2*margins[0], size[1]-2*margins[1])
		bg_rounded = AAfilledRoundedRect(bg_rect, self.bg_color, 0.04)

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
				#generate a Rect object of the right proportions (later converted to roundrect surface)
				square_rect = pygame.Rect(0,0, 0.2125*(size[0]-2*margins[0]), 0.2125*(size[1]-2*margins[1]))
				square_rounded = AAfilledRoundedRect(square_rect, self.colors[square], 0.1)
				surface.blit(square_rounded, (draw_x, draw_y))
				
				#draw text of value if square is not 0
				if square:
					#create and blit font surface
					font = pygame.font.SysFont("arial", int(size[1]/8))
					txt_color = self.txt_color_dark if (square <= 4) else self.txt_color_light
					txt_surface = font.render(str(square), True, txt_color)
					txt_coordinates = (draw_x+(0.2125*(size[0]-2*margins[0]))/4, draw_y+(0.2125*(size[1]-2*margins[1]))/20)
					surface.blit(txt_surface, txt_coordinates)

				draw_x += 0.2425*(size[0]-2*margins[0])

			draw_y += 0.2425*(size[1]-2*margins[1])

	#draws the entire board, by first drawing bg then squares
	def draw(self, surface, size, margins):
		self.draw_bg(surface, size, margins)
		self.draw_squares(surface, size, margins)

