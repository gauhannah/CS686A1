'''
	This class contains all information related to the state of
	the current path
'''

class State(object):
	def __init__(self, path):
		self.path = path
		self.g = 0
		self.h = 0
		self.f = 0



	def __eq__(self, other):
		return self.f == other.f

	def __lt__ (self, other):
		if self.f == other.f:
			return self.g < other.g
		return self.f < other.f

	def __gt__ (self, other):
		return other.__lt__(self)

	


