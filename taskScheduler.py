import requests
import asyncio
import os
import shutil


class TaskScheduler():
	def __init__(self, form, settings):
		self.settings = settings
		self.form = form
		self.task = {}
		self.task['install'] = []
		self.task['remove'] = []
		self.updateCount()
		pass

	def installMod(self, mod, version=None):
		if isinstance(mod, tuple):
			mod, version = mod
		if not mod.state['toInstall']:
			self.task['install'].append((mod, version))
			mod.state['toInstall'] = version
		else:
			task = self.getTaskByMod(mod, 'install')
			if task:
				mod.state['toInstall'] = False
				self.task['install'].remove(task)
		self.updateCount()

	def deleteMod(self, mod, version=None):
		if isinstance(mod, tuple):
			mod, version = mod
		version = mod.get("installed")
		if not mod.state['toDelete']:
			self.task['remove'].append((mod, version))
			mod.state['toDelete'] = version
		else:
			task = self.getTaskByMod(mod, 'remove')
			if task:
				mod.state['toDelete'] = False
				self.task['remove'].remove(task)
		self.updateCount()

	def deleteLocalMod(self, file):
		if not file in self.task['remove']:
			self.task['remove'].append(file)
		else:
			self.task['remove'].remove(file)
		self.updateCount()

	def updateMod(self, mod, version=None):
		if isinstance(mod, tuple):
			mod, version = mod
		if not mod.state['toUpdate']:
			self.task['install'].append((mod, version))
			self.task['remove'].append((mod, mod.get("installed")))
			mod.state['toUpdate'] = version
		else:
			task = self.getTaskByMod(mod, 'install')
			task2 = self.getTaskByMod(mod, 'remove')
			if task and task2:
				mod.state['toUpdate'] = False
				self.task['install'].remove(task)
				self.task['remove'].remove(task2)
		self.updateCount()

	def getTaskByMod(self, mod, task):
		for mods in self.task[task]:
			if mods[0] == mod:
				return mods
		return False

	def updateCount(self):
		self.form.taskCount.setText(
			f"<strong>To Install: </strong>{len(self.task['install'])}<br><strong>To Remove: </strong>{len(self.task['remove'])}")
		self.form.applyButton.setEnabled(
			not len(self.task["install"]) == len(self.task['remove']) == 0)

	def Apply(self, modList):
		maxValue = len(self.task["install"]) * 10 + len(self.task['remove']) * 1

		async def apply():
			currentValue = 0
			self.form.progressBar.setValue(0)
			for key in self.task["remove"]:
				if isinstance(key, str):
					if os.path.exists(self.settings.get("modDirPath") + key):
						os.remove(self.settings.get("modDirPath") + key)
				else:
					mod, version = key
					if os.path.exists(self.settings.get("modDirPath") + version.data['filename']):
						os.remove(self.settings.get("modDirPath") + version.data['filename'])
					mod.state = {"toInstall": False, "toDelete": False, "toUpdate": False, "installed": False}
					currentValue += 1
					self.form.progressBar.setValue(currentValue / maxValue * 100)
			self.task["remove"] = []
			for key in self.task["install"]:
				mod, version = key
				if os.path.isfile(self.settings.get("cacheDirPath") + version.data['filename']):
					shutil.copy(self.settings.get("cacheDirPath") + version.data['filename'],
								self.settings.get("modDirPath"))
				else:
					url = version.data['downloadLink']
					response = requests.get(
						url, headers={}, allow_redirects=True, verify=False)
					open(self.settings.get("cacheDirPath") + version.data['filename'], 'wb').write(response.content)
					shutil.copy(self.settings.get("cacheDirPath") + version.data['filename'],
								self.settings.get("modDirPath"))
				mod.state = {"toInstall": False, "toDelete": False, "toUpdate": False, "installed": version}
				currentValue += 10
				self.form.progressBar.setValue(currentValue / maxValue * 100)
			self.task["install"] = []
			self.updateCount()
			modList.updateModList()
			self.form.modList.setEnabled(True)
			modList.setMod()

		asyncio.run(apply())
