#imports
import pygame
from aaroundedrect import *
import random
import copy
from square import Square

class Board(object):

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
		512: (237, 200, 80),
		1024: (237, 196, 75),
		2048: (237, 192, 70),
	}
	txt_color_light = (249,247,243)
	txt_color_dark = (117, 109, 101)

	#inits the board
	def __init__(self):
		#stores the squares value
		self.squares = []

		#set all values to 0
		for i in range(4):
			self.squares.append([Square(0,(0,i)), Square(0,(1,i)), Square(0,(2,i)), Square(0,(3,i))])

	
	#changes positions according to core game mechanism in a certain direction
	#direction as string "up, down, left, right"
	#returns True if squares moved, False if none moved
	def move_in_direction(self, direction):
		"""
		core algorithm: 
		loop over row from side the row is moved towards
		if row is empty move to next
		if the next square is empty, move all others by one and repeat on same square until not empty or row empty 
		move through row, and repeat for all empty squares except empty end
		repeat loop over row
		if the next square is the same, merge them and move all others behind by one
		if the next square is non-empty non-identical, move to next square in loop

		up/down movement transposes the nested lists, moves right (down) or left (up) and transposes them back
		"""

		#stores a deepcopy of the board to check if any square moved later
		old_squares = copy.deepcopy(self.squares)

		#case switch the direction parameter
		if direction == "left":
			#loop over rows
			y = 0
			for x_row in self.squares:
				#jump to next row if empty (maybe remove later)
				row_empty = True
				for sq_obj in x_row:
					if sq_obj.value != 0:
						row_empty = False
				if row_empty:
					y += 1
					continue

				#loop over squares in row from left to right
				x = 0
				for sq_obj in x_row:

					"""
					if square is empty delete the list entry, append zero and repeat until not empty
					break if all following squares are empty
					NOTE: needs to use x_row[x] instead of square because iterating and modifying list at the same time
					"""
					while x_row[x].value == 0 and x <= 2:
						#move to next x if all others also empty
						rest_of_row_empty = True
						for n in range(x+1, 4):
							if not self.get_square((n,y)).value == 0:
								rest_of_row_empty = False
						if rest_of_row_empty:
								break

						#move all others by one
						del (self.squares[y][x])
						self.squares[y].append(Square(0,(x,y)))
					x += 1

				#repeat the loop over x-row after deleting empty
				x = 0
				for sq_obj in x_row:
					#if next square is the same, double it and contract the rest
					if x <= 2 and x_row[x].value == x_row[x+1].value:
						self.squares[y][x].value *= 2
						del(self.squares[y][x+1])
						self.squares[y].append(Square(0, (x,y)))
					x += 1
				y += 1

		elif direction == "up":
			#transpose
			self.squares = list(map(list, zip(*self.squares)))
			#move left
			self.move_in_direction("left")
			#transpose back
			self.squares = list(map(list, zip(*self.squares)))


		elif direction == "right":
			#loop over rows
			y = 0
			for x_row in self.squares:
				#jump to next row if empty (maybe remove later)
				row_empty = True
				for sq_obj in x_row:
					if sq_obj.value != 0:
						row_empty = False
				if row_empty:
					y += 1
					continue

				#loop over squares in row from right to left
				x = 3
				for sq_obj in x_row[::-1]:

					"""
					if square is empty delete the list entry, append zero and repeat until not empty
					break if all following squares are empty
					NOTE: needs to use x_row[x] instead of square because both iterating and modifying list
					"""
					while x_row[x].value == 0 and x >= 1:
						#move to next x if all others also empty
						rest_of_row_empty = True
						for n in range(0, x)[::-1]:
							if not self.get_square((n,y)).value == 0:
								rest_of_row_empty = False
						if rest_of_row_empty:
								break

						#move all others by one
						del (self.squares[y][x])
						self.squares[y].insert(0, Square(0,(x,y)))
					x -= 1

				#repeat the loop over x-row after deleting empty
				x = 3
				for sq_obj in x_row[::-1]:
					#if next square is the same, double it and contract the rest
					if x >= 1 and x_row[x].value == x_row[x-1].value:
						self.squares[y][x].value *= 2
						del(self.squares[y][x-1])
						self.squares[y].insert(0, Square(0, (x,y)))
					x -= 1
				y += 1

		elif direction == "down":
			#transpose
			self.squares = list(map(list, zip(*self.squares)))
			#move right
			self.move_in_direction("right")
			#transpose back
			self.squares = list(map(list, zip(*self.squares)))

		#compares the old deepcopy with the current board and returns if a square has moved
		square_moved = False
		old_square_values_flattened = [item.value for row in old_squares for item in row]
		new_square_values_flattened = [item.value for row in self.squares for item in row]
		if old_square_values_flattened != new_square_values_flattened:
			square_moved = True
		return square_moved

	#updates the x,y position and previous position for the square objects 
	def update_squares_position(self, surface, scr_size, margins):
		for y,x_row in enumerate(self.squares):
			for x,square in enumerate(x_row):
				square.previous_pos = square.pos
				square.pos = (x,y)
		self.animate_squares(surface, scr_size, margins)

	#returns true if two squares have the same value
	def same_value(self, position1, position2):
		return True if self.get_square(position1).value == self.get_square(position2).value else False

	#returns the value of a square
	def get_square(self, position):
		return self.squares[position[1]][position[0]]

	#returns true if the board is full and no further moves can be made, otherwise returns false
	def game_over(self):
		#deepcopy the board, move in all directions on the copied board and compare to original (after every move)
		board_same = True
		for direction in ["left", "up", "right", "down"]:
			board_copy = copy.deepcopy(self)
			board_copy.move_in_direction(direction)
			#repeated code, move into seperate function later
			old_square_values_flattened = [item.value for row in board_copy.squares for item in row]
			new_square_values_flattened = [item.value for row in self.squares for item in row]
			if (old_square_values_flattened != new_square_values_flattened):
				board_same = False
		return board_same

	#adds a random value of either 2 or 4 on an empty square, returns false if no empty squares
	def add_random_square(self):
		#return false if none empty (flatten array)
		flatten_squares = [item.value for sublist in self.squares for item in sublist]

		if not 0 in flatten_squares:
			return False

		#generate random pos until one is empty (if square value equals 0 while loop breaks)
		random_pos = (random.randint(0,3), random.randint(0,3))
		while self.squares[random_pos[1]][random_pos[0]].value:
			random_pos = (random.randint(0,3), random.randint(0,3))

		#add either 2 or 4, with a ration of 4 : 1
		new_value = random.choice((2,2,2,2,4))
		self.squares[random_pos[1]][random_pos[0]].value = new_value

		return True

	#add specific value to position for debugging purposes
	def add_square(self, value, position):
		self.squares[position[1]][position[0]].value = value

	#draws the background, blits a surface with dimensions (size, size)
	def draw_bg(self, surface, size, margins):
		bg_rect = pygame.Rect(0, 0, size[0]-2*margins[0], size[1]-2*margins[1])
		bg_rounded = AAfilledRoundedRect(bg_rect, self.bg_color, 0.04)
		surface.blit(bg_rounded, (margins[0], margins[1]))

		#draw empty squares
		for y in [0,1,2,3]:
			for x in [0,1,2,3]:
				draw_x = (margins[0]*0.955)+size[0]*0.03 + x*(0.2425*(size[0]-2*margins[0]))
				draw_y = (margins[1]*0.955)+size[1]*0.03 + y*(0.2425*(size[1]-2*margins[1]))
				square_rect = pygame.Rect(0,0, 0.2125*(size[0]-2*margins[0]), 0.2125*(size[1]-2*margins[1]))
				square_rounded = AAfilledRoundedRect(square_rect, self.colors[0], 0.1)
				surface.blit(square_rounded, (draw_x, draw_y))

	#draw the squares which make up the board
	def draw_squares(self, surface, size, margins):
		#distribute space: 5 x 4% empty, 4 x 20% square
		
		#iterate over board
		for x_row in self.squares:
			for sq_obj in x_row:
				#get the draw positions from the square object
				#start drawing at margin (mult. empirical factor!) + border width
				x,y = sq_obj.pos
				draw_x = (margins[0]*0.955)+size[0]*0.03 + x*(0.2425*(size[0]-2*margins[0]))
				draw_y = (margins[1]*0.955)+size[1]*0.03 + y*(0.2425*(size[1]-2*margins[1]))
				
				#draw square and text if square value is not 0
				if sq_obj.value:
					#generate a Rect object of the right proportions (later converted to roundrect surface)
					square_rect = pygame.Rect(0,0, 0.2125*(size[0]-2*margins[0]), 0.2125*(size[1]-2*margins[1]))
					square_rounded = AAfilledRoundedRect(square_rect, self.colors[sq_obj.value], 0.1)
					surface.blit(square_rounded, (draw_x, draw_y))
					#create and blit font surface
					font = pygame.font.SysFont("bold", int(size[1]/12))
					txt_color = self.txt_color_dark if (sq_obj.value <= 4) else self.txt_color_light
					txt_surface = font.render(str(sq_obj.value), True, txt_color)
					txt_x = draw_x+(0.2125*(size[0]-2*margins[0]))/2-0.5*txt_surface.get_width()
					txt_y = draw_y+(0.2125*(size[1]-2*margins[1]))/2-0.5*txt_surface.get_height()
					surface.blit(txt_surface, (txt_x, txt_y))

	#draws the entire board, by first drawing bg then squares
	def draw(self, surface, size, margins):
		self.draw_bg(surface, size, margins)
		self.draw_squares(surface, size, margins)
	

	"""
	The part below includes the methods for animating the movement
	still highly experimental
	
	Algorithm:
	- get the previous position and current position for a square
	- for animation_time loop the animation
	- if the previous position is "False" or equal to current skip the square
	- normalize the movement over the animation time
	- update draw_x for the square on each loop
	- draw the board with the temporary intermediate draw_pos

	"""
	def animate_squares(self, surface, scr_size, margins):
		#animation time in ms, framerate in 1/s
		animation_time = 1000
		framerate = 30

		#flatten the square objects nested array
		squares_flattened = [square for row in self.squares for square in row]
		squares_flattened_copy = [square for row in copy.deepcopy(self.squares) for square in row]
		squares_flattened_old_pos = [square.previous_pos for square in squares_flattened_copy]
		squares_flattened_new_pos = [square.pos for square in squares_flattened_copy]

		#initialize the animation
		time_elapsed = 0
		clock = pygame.time.Clock()

		while time_elapsed < animation_time:
			dt = clock.tick(framerate)
			time_elapsed += dt
			animation_progress = time_elapsed/animation_time

			#iterate over flattened squares and interpolate position from copied square values
			for index, square in enumerate(squares_flattened):
				if square.value != 0:
					square.pos = (squares_flattened_old_pos[index][0]+(squares_flattened_new_pos[index][0]-squares_flattened_old_pos[index][0])*animation_progress, squares_flattened_old_pos[index][1]+(squares_flattened_new_pos[index][1]-squares_flattened_old_pos[index][1])*animation_progress)

			self.draw(surface, scr_size, margins)
			pygame.display.update()

		#after animation fix square positions as animation causes small deviation
		for index, square in enumerate(squares_flattened):
			square.pos = (squares_flattened_new_pos[index][0], squares_flattened_new_pos[index][1])