class ModVersion():
	def __init__(self, data):
		self.data = data
		self.latest = False
	def __str__(self):
		return self.data['version']
	def get(self, value):
		return self.data[value]