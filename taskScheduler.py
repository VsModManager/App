
class TaskScheduler():
	def __init__(self, form):
		self.form = form
		self.task = {}
		self.task['install'] = []
		self.task['remove'] = []
		
		pass

	def installMod(self, mod, version = None):
		if isinstance(mod, tuple):
			mod, version = mod
		print(mod.data["name"])
		print(version["version"],version["latest"])
		updateCount(self)

	def deleteMod(self, mod, version = None):
		if isinstance(mod, tuple):
			mod, version = mod
		updateCount(self)

	def updateMod(self, mod, version = None):
		if isinstance(mod, tuple):
			mod, version = mod
		updateCount(self)

	def updateCount(self):
		self.form.taskCount.setText(f"<strong>To Install: </strong>{len(self.task.install)}<br><strong>To Remove: </strong>{len(self.task.remove)}")

	def Apply(self):
		.setMaximum
		pass