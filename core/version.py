from core import model


class version(model.model):
	table = 'version'

	def __init__(self, manager, criteria=None):
		super().__init__()
		self.criteria = criteria
		self.manager = manager

	pass
