#imports
import pygame
from aaroundedrect import *
import random

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

	#inits the board
	def __init__(self):

		#set all values to 0
		for i in range(4):
			self.squares.append([0, 0, 0, 0])

	
	#changes positions when the game moves in a certain direction
	#direction as string "up, down, left, right"
	def move_in_direction(self, direction):
		"""
		core algorithm: 
		loop over row/column from side the row/column is moved towards (requires transposing or creating y_column for up/down)
		if row is empty move to next
		if the next square is empty, move all others by one and repeat on same square until not empty or row empty 
		move through row, and repeat for all empty squares except empty end
		repeat loop over row
		if the next square is the same, merge them and move all others behind by one
		if the next square is non-empty non-identical, move to next square in loop
		"""

		#case switch the direction parameter
		if direction == "left":
			#loop over rows
			y = 0
			for x_row in self.squares:
				#jump to next row if empty
				if  x_row == [0,0,0,0]:
					y += 1
					continue

				#loop over squares in row (except last)
				x = 0
				for square in x_row:

					"""
					if square is empty delete the list entry, append zero and repeat until not empty
					break if all following squares are empty
					NOTE: needs to use x_row[x] instead of square because both iterating and modifying list
					"""
					while x_row[x] == 0 and x <= 2:
						#move to next x if all others also empty
						rest_of_row_empty = True
						for n in range(x+1, 4):
							if not self.get_square((n,y)) == 0:
								rest_of_row_empty = False
						if rest_of_row_empty:
								break

						#move all others by one
						del (self.squares[y][x])
						self.squares[y].append(0)
					x += 1

				#repeat the loop over x-row after deleting empty
				x = 0
				for square in x_row:
					#if next square is the same, double it and contract the rest
					if x <= 2 and x_row[x] == x_row[x+1]:
						self.squares[y][x] *= 2
						del(self.squares[y][x+1])
						self.squares[y].append(0)
					x += 1
				y += 1

		elif direction == "up":
			pass

		elif direction == "right":
			pass

		elif direction == "left":
			pass

	#returns true if two squares have the same value
	def same_value(self, position1, position2):
		return True if self.get_square(position1) == self.get_square(position2) else False

	#returns the value of a square
	def get_square(self, position):
		return self.squares[position[1]][position[0]]


	#adds a random value of either 2 or 4 on an empty square, returns false if no empty squares
	def add_random_square(self):
		#return false if none empty (flatten array)
		flatten_squares = [item for sublist in self.squares for item in sublist]

		if not 0 in flatten_squares:
			return False

		#generate random pos until one is empty (if square value equals 0 while loop breaks)
		random_pos = (random.randint(0,3), random.randint(0,3))
		while self.squares[random_pos[1]][random_pos[0]]:
			random_pos = (random.randint(0,3), random.randint(0,3))

		#add either 2 or 4, with a ration of 4 : 1
		new_value = random.choice((2,2,2,2,4))
		self.squares[random_pos[1]][random_pos[0]] = new_value

		return True

	#add specific value to position for debugging purposes
	def add_square(self, value, position):
		self.squares[position[1]][position[0]] = value

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

