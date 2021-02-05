class ModVersion():
	def __init__(self, data):
		self.data = data
		self.latest = False

	def compare(self, version=False):
		if not version: return 0
		if self.index > version.index: return -1
		if self.index < version.index: return 1
		return 0

	def __str__(self):
		return self.data['version']

	def get(self, value):
		return self.data[value]
