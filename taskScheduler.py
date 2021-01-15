import requests
from time import sleep

class TaskScheduler():
	def __init__(self, form, moddir):
		self.form = form
		self.moddir = moddir
		self.task = {}
		self.task['install'] = []
		self.task['remove'] = []
		self.updateCount()
		pass

	def installMod(self, mod, version = None):
		if isinstance(mod, tuple):
			mod, version = mod
		self.task['install'].append((mod, version))
		mod.state['toInstall'] = version
		self.updateCount()

	def deleteMod(self, mod, version = None):
		if isinstance(mod, tuple):
			mod, version = mod
		self.updateCount()

	def updateMod(self, mod, version = None):
		if isinstance(mod, tuple):
			mod, version = mod
		self.updateCount()

	def updateCount(self):
		self.form.taskCount.setText(
			f"<strong>To Install: </strong>{len(self.task['install'])}<br><strong>To Remove: </strong>{len(self.task['remove'])}")
		self.form.applyButton.setEnabled(
			not len(self.task["install"]) == len(self.task['remove']) == 0)

	def Apply(self, modList):
		maxValue = len(self.task["install"]) * 10 + len(self.task['remove']) * 5
		currentValue = 0
		self.form.progressBar.setValue(0)
		for key in self.task["install"]:
			sleep(.5)
			mod, version = key
			url = version.data['downloadLink']
			response = requests.get(
				url, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True)
			open(self.moddir + version.data['filename'], 'wb').write(response.content)
			currentValue += 10
			self.form.progressBar.setValue(currentValue / maxValue * 100)
		self.form.modList.setEnabled(True)
		modList.setMod()
