class Square(object):

	#inits with square value as int and position as tuple (x,y)
	def __init__(self, value, position):
		self.value = value
		self.pos = position

	#returns the exact x,y coordinates for drawing
	def get_draw_pos(self, margins, scr_size):
		x,y = self.pos
		#start drawing at y_margin (mult. empirical factor!) + top border width
		#start drawing at x_margin (mult. empirical factor!) + left border width
		draw_x = (margins[0]*0.955)+scr_size[0]*0.03 + x*(0.2425*(scr_size[0]-2*margins[0]))
		draw_y = (margins[1]*0.955)+scr_size[1]*0.03 + y*(0.2425*(scr_size[1]-2*margins[1]))

		return (draw_x, draw_y)

	#returns the position for the font to be drawn
	def get_text_draw_pos(self, margins, scr_size, txt_surface):
		draw_x, draw_y = self.get_draw_pos(margins, scr_size)
		txt_x = draw_x+(0.2125*(scr_size[0]-2*margins[0]))/2-0.5*txt_surface.get_width()
		txt_y = draw_y+(0.2125*(scr_size[1]-2*margins[1]))/2-0.5*txt_surface.get_height()
		return txt_x,txt_y
