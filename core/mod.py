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

	def getLastVersion(self):
		criteria = {'mod': self.get('id'), 'version': self.get('lastVersion')}
		return self.manager.getObject('version', criteria)
		pass

	def getVersions(self):
		criteria = {'mod': self.get('id')}
		return self.manager.getIterator('version', criteria)
		pass
