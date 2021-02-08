from core import model


class mod(model.model):
	table = 'mod'

	def __init__(self, manager, criteria=None):
		super().__init__()
		self.manager = manager
		self.process()
		if criteria:
			self.criteria = self.criteria2where(criteria)
			self.initialize()

	pass
