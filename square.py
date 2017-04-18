class Square(object):

	#inits with square value as int and position as tuple (x,y)
	def __init__(self, value, position):
		self.value = value
		self.pos = position
		self.previous_pos = False