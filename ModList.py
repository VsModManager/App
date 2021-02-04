from Mod import Mod
from taskScheduler import TaskScheduler
from presets import presets
from time import sleep
import datetime
import hashlib
import json
import requests
import os
import asyncio
from PyQt5.QtGui import QPixmap

from TableModel import TableModel


class ModList():
	def __init__(self, form, settings, host, filename='modListData.json'):
		self.settings = settings
		self.presets = presets(form, settings)
		self.filename = self.settings.get("modListDataFile")
		self.form = form
		self.host = host
		self.moddir = self.settings.get("modDirPath")
		self.TaskScheduler = TaskScheduler(self.form, self.settings)
		sleep(0.1)
		form.progressBar.setValue(20)
		if (os.path.isfile(self.filename)):
			self.compareHash(form.progressBar)
		else:
			sleep(0.1)
			form.progressBar.setValue(40)
			self.downloadModList()
			sleep(0.05)
			form.progressBar.setValue(60)
		self.mods = []
		sleep(0.1)
		form.progressBar.setValue(90)
		self.generateModList()
		self.updateModList()
		self.defaultMod = self.mods[0]
		self.selectedMod = self.defaultMod
		sleep(0.05)
		form.progressBar.setValue(100)

	def updateModList(self):
		self.TableModel.setNewData(self.renderList())
		print("updateModList")
		self.form.modList.setModel(self.TableModel)

	def compareHash(self, progressBar):
		response = requests.request("POST", self.host, headers={}, verify=False, data={
			'hash': self.md5File()
		})
		if response.status_code == 200:
			self.settings.local = False
			if json.loads(response.text)['success'] or True:
				sleep(0.05)
				progressBar.setValue(40)
				sleep(0.05)
				progressBar.setValue(60)
				print("HASH matches")
				self.loadFile()
			else:
				sleep(0.1)
				progressBar.setValue(40)
				self.downloadModList()
				sleep(0.1)
				progressBar.setValue(60)
				print("HASH updated")
			return self
		print("unableToConnectToServer")
		self.settings.local = True
		sleep(0.2)
		progressBar.setValue(40)
		sleep(0.1)
		progressBar.setValue(60)
		self.loadFile()
		return self

	def downloadModList(self):
		response = requests.request(
			"GET", self.host, headers={}, data={}, verify=False)
		file = open(self.filename, 'w+', encoding='utf-8')
		self.rawData = json.loads(response.text)
		file.write(response.text)

		# self.rawData = json.load(open('mod.json', 'r', encoding='utf-8'))

	def loadFile(self):
		self.rawData = json.load(open(self.filename, 'r', encoding='utf-8'))
		return self.rawData

	def md5File(self):
		hash_md5 = hashlib.md5()
		with open(self.filename, "rb") as f:
			for chunk in iter(lambda: f.read(4096), b""):
				hash_md5.update(chunk)
		return hash_md5.hexdigest()

	def generateModList(self):
		_, _, installed = next(os.walk(self.moddir))
		for mod in self.rawData:
			self.mods.append(Mod(mod, installed))

		def modListClicked(selected, deselected):
			index = self.form.modList.model().index(selected.row(), 7)
			self.setMod(int(index.data()))
		self.TableModel = TableModel(self.form.modList, self.renderList(
		), ['', 'Name', 'Author', 'Raiting', 'Downloads', 'Version', 'gameversion', ''])
		self.form.modList.setModel(self.TableModel)
		self.form.modList.selectionModel().currentRowChanged.connect(modListClicked)
		self.form.modList.selectRow(0)

	def clearCache(self):
		for file in os.listdir(self.settings.get("cacheDirPath")):
			if self.settings.get("saveCache") == 0:
				if os.path.isfile(self.settings.get("cacheDirPath") + file) and file.endswith('.zip'):
					if datetime.datetime.fromtimestamp(os.stat(self.settings.get("cacheDirPath") + file).st_atime) + datetime.timedelta(days=self.settings.get("saveCache")) < datetime.datetime.now():
						os.remove(self.settings.get("cacheDirPath") + file)

	def renderList(self):
		renderList = []
		for mod in self.mods:
			renderList.append(mod.render())
		return renderList

	def getByID(self, id):
		for mod in self.mods:
			if mod.data['id'] == id:
				return mod
		return self.defaultMod

	def setMod(self, id=False):
		if not isinstance(id, bool):
			self.selectedMod = self.getByID(id)
			self.form.comboBox.clear()
			self.form.comboBox.addItem("Latest")
			self.form.comboBox.addItems(self.selectedMod.versions)
			asyncio.run(self.render())
			# self.render()

		self.renderButtons()
		# self.form.<img src="">
		# Installed

	async def render(self):
		self.form.modName.setText(self.selectedMod.get('name', 'Unknown'))
		self.form.modDesc.setText(self.selectedMod.get('description', self.settings.get('language')))
		def getLine(x, y):
			return f"<strong>{x}: </strong>{y}<br>"
		modInfo = ""
		modInfo += getLine("Author", self.selectedMod.get('authors', 'Unknown'))
		modInfo += getLine("Downloads", self.selectedMod.get('downloads', 'Unknown'))
		modInfo += getLine("Raiting", self.selectedMod.get('raiting', 'Unknown'))
		modInfo += getLine("Tags", self.selectedMod.get('tags'))

		modInfo += f"<br>{self.selectedMod.get('shotDescription', 'en')}"

		# modInfo += f"<strong>Views: </strong>{self.selectedMod.get('views', 'Unknown')}<br>"
		self.form.modInfo.setText(modInfo)
		if self.selectedMod.get("img") == False:
			self.form.image.setText("")
		else:
			imageFile = self.settings.get("imageDirPath") + "m" + str(self.selectedMod.get('id'))
			if not os.path.isfile(imageFile):
				url = self.selectedMod.get("img")
				response = requests.get(url, headers={}, allow_redirects=True, verify=False)
				open(imageFile, 'wb').write(response.content)
			
			width = self.form.image.frameGeometry().width()
			height = self.form.image.frameGeometry().height()

			pixmap = QPixmap(imageFile).scaled(width, height, 1)
			# pixmap = pixmap
			self.form.image.setPixmap(pixmap)

	def renderButtons(self):
		_, selected = self.selectMod()
		version = self.selectedMod.get('installed')
		toBeInstalled = self.selectedMod.get('toInstall')
		toBeRemoved = self.selectedMod.get('toDelete')
		toBeUpdated = self.selectedMod.get('toUpdate')
		update = (toBeUpdated or selected).compare(version)
		latest = ""
		latestV = ""

		if toBeInstalled:
			self.form.installButton.setText("Cancel")
			self.form.installButton.setEnabled(True)
		elif version:
			self.form.installButton.setText("Install")
			self.form.installButton.setEnabled(False)
		else:
			self.form.installButton.setText("Install")
			self.form.installButton.setEnabled(True)

		if toBeRemoved:
			self.form.deleteButton.setText("Cancel")
			self.form.deleteButton.setEnabled(True)
		elif version:
			self.form.deleteButton.setText("Uninstall")
			self.form.deleteButton.setEnabled(True)
		else:
			self.form.deleteButton.setText("Uninstall")
			self.form.deleteButton.setEnabled(False)

		if not toBeUpdated and (not version or update == 0):
			self.form.updateButton.setText('Upgrade')
			self.form.updateButton.setEnabled(False)
		elif toBeUpdated:
			self.form.updateButton.setText('Cancel')
			self.form.updateButton.setEnabled(True)
		elif toBeRemoved or toBeInstalled:
			self.form.updateButton.setText(update == -1 and 'Downgrade' or 'Upgrade')
			self.form.updateButton.setEnabled(False)
		else:
			self.form.updateButton.setText(update == -1 and 'Downgrade' or 'Upgrade')
			self.form.updateButton.setEnabled(True)

		if self.settings.local:
			self.form.updateButton.setEnabled(False)
			self.form.installButton.setEnabled(False)

		if version:
			latest = version.latest and "(Latest)"
		if toBeInstalled or toBeUpdated:
			latestV = (toBeInstalled or toBeUpdated).latest and "(Latest)"

		text = f"<strong>Installed: </strong>{version or 'None'} {version and latest or ''}<br>"

		if self.settings.local:
			text += "unable connect to server"
		elif not (toBeInstalled or toBeRemoved or toBeUpdated):
			text += " "
		elif toBeUpdated:
			text += f"<strong>{update==-1 and 'Downgrade' or 'Upgrade'} To: </strong>{toBeUpdated} {latestV or ''}"
		else:
			text += f"<strong>To be {toBeRemoved and 'removed' or 'installed'}: </strong>{toBeInstalled or toBeRemoved} {toBeInstalled and latest or ''}"

		# 	self.form.deleteButton.setEnabled(True)
		# else:
		# 	self.form.deleteButton.setEnabled(False)

		# if version == toBeInstalled:
		# 	self.form.installButton.setText("Cancel")
		# else:
		# 	self.form.installButton.setText("Install")
		# if version != toBeInstalled and version and toBeInstalled:

		self.form.deleteText.setText(text)

		self.form.comboBox.setEnabled(True)

	def selectMod(self):
		select = self.form.comboBox.currentIndex()
		version = None
		if select <= 0:
			version = self.selectedMod.getLastVersion()
		else:
			version = self.selectedMod.getVersion(self.selectedMod.versions[select - 1])
		return (self.selectedMod, version)

	def installMod(self):
		self.TaskScheduler.installMod(self.selectMod())
		self.setMod()

	def deleteMod(self):
		self.TaskScheduler.deleteMod(self.selectMod())
		self.setMod()

	def updateMod(self):
		self.TaskScheduler.updateMod(self.selectMod())
		self.setMod()

	def applyMods(self):
		self.form.deleteButton.setEnabled(False)
		self.form.installButton.setEnabled(False)
		self.form.updateButton.setEnabled(False)
		self.form.applyButton.setEnabled(False)
		self.form.comboBox.setEnabled(False)
		self.form.modList.setEnabled(False)
		self.TaskScheduler.Apply(self)

	def downloadMod(self):
		self.selectedMod.download()
		pass
