#imports
import pygame
from aaroundedrect import *
import random
import copy
from square import Square

#board instance has a 2D list (4x4) attribute holding the square objects
#board class has methods for game movement, drawing, controlling square values
#board instance is controlled directly from 2048.py
class Board(object):
	#color values
	bg_color = (187, 173, 160)
	txt_color_light = (249,247,243)
	txt_color_dark = (117, 109, 101)
	square_colors = {
		0: (205, 192, 180),
		2: (238, 228, 218),
		4: (237, 224, 200),
		8: (242, 177, 121),
		16: (245, 150, 99),
		32: (246, 124, 95),
		64: (246, 107, 65),
		128: (237, 208, 114),
		256: (237, 204, 97),
		512: (237, 200, 80),
		1024: (237, 196, 75),
		2048: (237, 192, 70),
	}

	#inits the board with surface to draw to and scr_size and margin attributes
	#has attributes for Pygame font and rect surface as these otherwise need to be generated frequently
	#creates a 4x4 grid and fills it with square objects with value 0
	def __init__(self, surface, scr_size, margins):
		self.surface = surface
		self.scr_size = scr_size
		self.margins = margins
		self.font = pygame.font.SysFont("bold", int(scr_size[1]/12))
		self.square_rect = pygame.Rect(0,0, 0.2125*(scr_size[0]-2*margins[0]), 0.2125*(scr_size[1]-2*margins[1]))
		self.square_rect_size = 0.2125*(scr_size[0]-2*margins[0])
		self.rounded_empty_square = AAfilledRoundedRect(self.square_rect, self.square_colors[0], 0.1)

		#creates the 4x4 squares grid as a 2D list
		self.squares = []
		for i in [0,1,2,3]:
			self.squares.append([Square(0,(0,i)), Square(0,(1,i)), Square(0,(2,i)), Square(0,(3,i))])
	
	#changes positions according to core game mechanism in a certain direction
	#takes direction parameter as string "up, down, left, right" (keys bindings in 2048.py)
	#returns True if squares moved, False if none moved which is checked by deepcopying the board
	def move_in_direction(self, direction):
		"""
		core algorithm: 
		loop over each row twice starting from side moved towards, first time deleting empty squares second time merging identical squares
		implemented for left/right movement. Up/down transposes the board, moves right (down) or left (up) and transposes back

		implementation pseudocode
		- iterate rows in grid
		- iterate squares in row starting from side the row is moved towards
		- if the square is empty, delete it and append empty square at end
		- repeat on same square until not either empty anymore (move to next square) or row empty (move to next row)
		- iterate squares in row second time
		- if the next square is the same, merge them, delete the next square and append empty square
		- if the next square is non-empty non-identical, move to next square in iteration

		check if a move was made by comparing new board to old deepcopy of board (flatten grid and store square values in list)
		"""

		#stores a deepcopy of the board to check if any square moved later
		old_square_values_flattened = [square.value for row in copy.deepcopy(self.squares) for square in row]

		#case switch the direction parameter
		if direction == "left":
			#iterate rows
			y = 0
			for x_row in self.squares:
				#iterate squares in row first time deleting empty squares
				x = 0
				for sq_obj in x_row:
					"""
					if square is empty delete the list entry, append zero and repeat until not empty
					break if all following squares are empty
					NOTE: needs to use x_row[x] instead of sq_obj because iterating and modifying list at the same time
					"""
					while x_row[x].value == 0 and x <= 2:
						#move to next row if all others also empty
						rest_of_row_empty = True
						for n in range(x+1, 4):
							if not self.get_square((n,y)).value == 0:
								rest_of_row_empty = False
						if rest_of_row_empty:
								break

						#delete current empty square and add new empty square to end of row
						del (self.squares[y][x])
						self.squares[y].append(Square(0,(x,y)))
					x += 1

				#repeat the loop over x-row after deleting empty
				x = 0
				for sq_obj in x_row:
					#if next square is the same, double it, delete the next and add empty square to end of row
					if x <= 2 and x_row[x].value == x_row[x+1].value:
						self.squares[y][x].value *= 2
						self.squares[y][x].was_doubled = True
						del(self.squares[y][x+1])
						self.squares[y].append(Square(0, (x,y)))
					x += 1
				y += 1

		elif direction == "up":
			#transpose, move left, transpose back
			self.squares = list(map(list, zip(*self.squares)))
			self.move_in_direction("left")
			self.squares = list(map(list, zip(*self.squares)))


		elif direction == "right":
			#iterate rows
			y = 0
			for x_row in self.squares:
				#loop over squares in row from right to left
				x = 3
				for sq_obj in x_row[::-1]:
					"""
					if square is empty delete the list entry, append zero and repeat until not empty
					break if all following squares are empty
					NOTE: needs to use x_row[x] instead of sq_obj because iterating and modifying list at the same time
					"""
					while x_row[x].value == 0 and x >= 1:
						#move to next row if all others also empty
						rest_of_row_empty = True
						for n in range(0, x)[::-1]:
							if not self.get_square((n,y)).value == 0:
								rest_of_row_empty = False
						if rest_of_row_empty:
								break

						#delete current empty square and add new empty square to beginning of row
						del (self.squares[y][x])
						self.squares[y].insert(0, Square(0,(x,y)))
					x -= 1

				#repeat the loop over x-row after deleting empty
				x = 3
				for sq_obj in x_row[::-1]:
					#if next square is the same, double it, delete the next and add empty square to beginning of row
					if x >= 1 and x_row[x].value == x_row[x-1].value:
						self.squares[y][x].value *= 2
						self.squares[y][x].was_doubled = True
						del(self.squares[y][x-1])
						self.squares[y].insert(0, Square(0, (x,y)))
					x -= 1
				y += 1

		elif direction == "down":
			#transpose, move left, transpose back
			self.squares = list(map(list, zip(*self.squares)))
			self.move_in_direction("right")
			self.squares = list(map(list, zip(*self.squares)))

		#compares the old deepcopy values with the current board and returns true if a square has moved, false if not
		square_moved = False
		new_square_values_flattened = [square.value for row in self.squares for square in row]
		if old_square_values_flattened != new_square_values_flattened:
			square_moved = True
		return square_moved

	#updates the x,y position and previous position for the square objects 
	#triggers the animation for the movement
	def update_squares_position(self):
		#iterate squares
		for y,x_row in enumerate(self.squares):
			for x,square in enumerate(x_row):
				#store the last position of the square in the according attribute
				square.previous_pos = square.pos
				square.pos = (x,y)
				#for empty squares the previous position is the current position
				#this is necessary because the "move_in_direction" method deletes and moves empty square objects
				if square.value == 0:
					square.previous_pos = (x,y)

		self.animate_squares()

	#returns true if two squares have the same value
	def same_value(self, position1, position2):
		return True if self.get_square(position1).value == self.get_square(position2).value else False

	#returns the square object at position (x,y)
	def get_square(self, position):
		return self.squares[position[1]][position[0]]

	#returns true if the board is full and no further moves can be made, otherwise returns false
	def game_over(self):
		#deepcopy the board squares, move in all directions on the copied board and compare to original (after every move)
		#NOTE: cannot deepcopy board directly because it has a Pyame surface as attribute which cannot be deepcopied
		for direction in ["left", "up", "right", "down"]:
			board_copy = Board(self.surface, self.scr_size, self.margins)
			board_copy.squares = copy.deepcopy(self.squares)
			board_copy.move_in_direction(direction)
			#repeated code, move into seperate function later
			old_square_values_flattened = [item.value for row in board_copy.squares for item in row]
			new_square_values_flattened = [item.value for row in self.squares for item in row]
			if (old_square_values_flattened != new_square_values_flattened):
				return False
		return True

	#adds a random value of either 2 or 4 on an empty square, returns False if no empty squares otherwise True
	def add_random_square(self):
		#return False if no value 0 in flattened squares grid
		if not 0 in [square.value for row in self.squares for square in row]:
			return False

		#generate random pos until one is empty (if square value equals 0 while loop breaks)
		random_pos = (random.randint(0,3), random.randint(0,3))
		while self.squares[random_pos[1]][random_pos[0]].value:
			random_pos = (random.randint(0,3), random.randint(0,3))

		#add either 2 or 4, with a ration of 4 : 1
		new_value = random.choice((2,2,2,2,4))
		self.squares[random_pos[1]][random_pos[0]].value = new_value

		return True

	#draws the background, blits a surface with dimensions (scr_size)
	def draw_bg(self):
		bg_rect = pygame.Rect(0, 0, self.scr_size[0]-2*self.margins[0], self.scr_size[1]-2*self.margins[1])
		bg_rounded = AAfilledRoundedRect(bg_rect, self.bg_color, 0.04)
		self.surface.blit(bg_rounded, (self.margins[0], self.margins[1]))

		#draw empty squares
		for y in [0,1,2,3]:
			for x in [0,1,2,3]:
				self.surface.blit(self.rounded_empty_square, self.get_draw_pos((x,y)))

	#draw the squares which make up the board
	#distribute space: 5 x 4% empty, 4 x 20% square
	def draw_squares(self):
		#iterate squares
		for x_row in self.squares:
			for sq_obj in x_row:				
				#draw square and text if square value is not 0
				if sq_obj.value:
					draw_x, draw_y = self.get_draw_pos(sq_obj.pos)					

					#convert the square_rect attribute to a rounded rect surface, get the color form square_color dict
					#if the square object has a modified resize_factor attribute modify the pygame.Rect accordingly				
					modify_rect_size = self.square_rect_size*(sq_obj.resize_factor-1)
					draw_x -= modify_rect_size*0.5
					draw_y -= modify_rect_size*0.5
					square_rounded = AAfilledRoundedRect(self.square_rect.inflate(modify_rect_size, modify_rect_size), self.square_colors[sq_obj.value], 0.1)
					self.surface.blit(square_rounded, (draw_x, draw_y))
					#create and blit font surface
					txt_color = self.txt_color_dark if (sq_obj.value <= 4) else self.txt_color_light
					txt_surface = self.font.render(str(sq_obj.value), True, txt_color)
					txt_x = draw_x+modify_rect_size*0.5+(0.2125*(self.scr_size[0]-2*self.margins[0]))/2-0.5*txt_surface.get_width()
					txt_y = draw_y+modify_rect_size*0.5+(0.2125*(self.scr_size[1]-2*self.margins[1]))/2-0.5*txt_surface.get_height()
					self.surface.blit(txt_surface, (txt_x, txt_y))

	#draws the entire board, by first drawing bg followed by squares
	def draw(self):
		self.draw_bg()
		self.draw_squares()
	
	#returns the position (x,y) for drawing a square
	def get_draw_pos(self, pos):
		#start drawing at margin (mult. empirical factor!) + border width
		draw_x = (self.margins[0]*0.955)+self.scr_size[0]*0.03 + pos[0]*(0.2425*(self.scr_size[0]-2*self.margins[0]))
		draw_y = (self.margins[1]*0.955)+self.scr_size[1]*0.03 + pos[1]*(0.2425*(self.scr_size[1]-2*self.margins[1]))
		return (draw_x,draw_y)

	#animates the movement of squares after updating square values, before adding new square
	def animate_squares(self):
		"""
		Algorithm:
		- get the previous position and current position for a square
		- for animation_time loop the animation
		- if the previous position is "False" or equal to current skip the square
		- normalize the movement over the animation time
		- update draw_x for the square on each loop
		- draw the board with the temporary intermediate draw_pos
		"""

		#flatten the square objects nested array
		squares_flattened = [square for row in self.squares for square in row]
		squares_flattened_copy = copy.deepcopy(squares_flattened)
		squares_flattened_old_pos = [square.previous_pos for square in squares_flattened_copy]
		squares_flattened_new_pos = [square.pos for square in squares_flattened_copy]

		#initialize the animation. animation/elapsed time in ms, framerate in 1/s
		animation_time = 100
		framerate = 100
		time_elapsed = 0
		clock = pygame.time.Clock()

		#animation loop
		while time_elapsed < animation_time:
			dt = clock.tick(framerate)
			animation_progress = time_elapsed/animation_time

			#iterate over flattened squares and interpolate position from copied square values and modify resize for doubled squares
			for index, square in enumerate(squares_flattened):
				if square.value != 0:
					x_old, y_old = squares_flattened_old_pos[index]
					x_new, y_new = squares_flattened_new_pos[index]
					square.pos = (x_old+(x_new-x_old)*animation_progress, y_old+(y_new-y_old)*animation_progress)

					#size increases and decreases as animation progresses
					if square.was_doubled:
						square.resize_factor = 1+0.4*(0.5-abs(0.5-animation_progress))

			time_elapsed += dt

			self.draw()
			pygame.display.update()

		#after animation fix square positions as animation causes small deviation
		#set was_doubled attribute back to false
		for index, square in enumerate(squares_flattened):
			square.pos = (squares_flattened_new_pos[index][0], squares_flattened_new_pos[index][1])
			square.was_doubled = False
			square.resize_factor = 1.0