from Mod import Mod
from taskScheduler import TaskScheduler
from time import sleep
import hashlib
import json
import requests
import numpy as np
from os.path import isfile
from os import walk
import pandas as pd
from TableModel import TableModel


class ModList():
	def __init__(self, form, moddir, host, filename='modListData.json'):
		self.filename = filename
		progressBar = form.progressBar
		self.form = form
		self.host = host
		self.moddir = moddir
		self.TaskScheduler = TaskScheduler(self.form, self.moddir)
		sleep(0.1)
		progressBar.setValue(20)
		if (isfile(self.filename)):
			self.compareHash(progressBar)
		else:
			sleep(0.1)
			progressBar.setValue(40)
			self.downloadModList()
			sleep(0.05)
			progressBar.setValue(60)
		self.mods = []
		sleep(0.1)
		progressBar.setValue(90)
		self.generateModList()
		self.updateModList()
		self.defaultMod = self.mods[0]
		self.selectedMod = self.defaultMod
		sleep(0.05)
		progressBar.setValue(100)

	def updateModList(self):
		def modListClicked(selected, deselected):
			index = self.form.modList.model().index(selected.row(), 6)
			self.setMod(int(index.data()))
		data = pd.DataFrame(self.render(), columns = ['', 'Name', 'Author', 'Downloads', 'Version', 'gameversion', ''])
		self.form.modList.setModel(TableModel(data))
		self.form.modList.selectionModel().currentRowChanged.connect(modListClicked)
		self.form.modList.selectRow(0)

	def compareHash(self, progressBar):
		response = requests.request("POST", self.host, headers={}, data={
			'hash': self.md5File()
		})
		if response.status_code == 200:
			if json.loads(response.text)['success']:
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
		sleep(0.2)
		progressBar.setValue(40)
		sleep(0.1)
		progressBar.setValue(60)
		self.loadFile()
		return self

	def downloadModList(self):
		response = requests.request("GET", self.host, headers={}, data={})
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
		_, _, installed = next(walk(self.moddir))
		for mod in self.rawData:
			self.mods.append(Mod(mod, installed))

	def render(self):
		renderList = []
		for mod in self.mods:
			renderList.append(mod.render())
		return renderList

	def getByID(self, id):
		for mod in self.mods:
			if mod.data['id'] == id:
				return mod
		return self.defaultMod

	def setMod(self, id = False):
		if not isinstance(id, bool):
			self.selectedMod = self.getByID(id)
		# else:
			self.form.comboBox.clear()
			self.form.comboBox.addItem("Latest")
			self.form.comboBox.addItems(self.selectedMod.versions)
			self.form.modName.setText(self.selectedMod.get('name', 'Unknown'))
			self.form.modDesc.setText(self.selectedMod.get('description', 'Unknown'))
			modInfo = ""
			modInfo += f"<strong>Author: </strong>{self.selectedMod.get('authors', 'Unknown')}<br>"
			modInfo += f"<strong>Downloads: </strong>{self.selectedMod.get('downloads', 'Unknown')}<br>"
			# modInfo += f"<strong>Views: </strong>{self.selectedMod.get('views', 'Unknown')}<br>"
			self.form.modInfo.setText(modInfo)
		self.renderButtons()
		# self.form.<img src="">
		# Installed
	def renderButtons(self):
		_, selected = self.selectMod()
		version = self.selectedMod.get('installed')
		toBeInstalled = self.selectedMod.get('toInstall')
		toBeRemoved = self.selectedMod.get('toDelete')
		toBeUpdated = self.selectedMod.get('toUpdate')
		update = selected.compare(version)
		latest = ""

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

		if not version or update == 0:
			self.form.updateButton.setText('Upgrade')
			self.form.updateButton.setEnabled(False)
		elif toBeUpdated:
			self.form.updateButton.setText('Cancel')
			self.form.updateButton.setEnabled(True)
		elif toBeRemoved or toBeInstalled:
			self.form.updateButton.setText(update==-1 and 'Downgrade' or 'Upgrade')
			self.form.updateButton.setEnabled(False)
		else:
			self.form.updateButton.setText(update==-1 and 'Downgrade' or 'Upgrade')
			self.form.updateButton.setEnabled(True)

		if version or toBeInstalled or toBeUpdated:
			latest = (version or toBeInstalled or toBeUpdated).latest and "(Latest)"
		# 	self.form.deleteButton.setEnabled(True)
		# else:
		# 	self.form.deleteButton.setEnabled(False)

		# if version == toBeInstalled:
		# 	self.form.installButton.setText("Cancel")
		# else:
		# 	self.form.installButton.setText("Install")
		# if version != toBeInstalled and version and toBeInstalled:

		self.form.deleteText.setText(
			f"<strong>Installed: </strong>{version or 'None'} {version and latest or ''}<br>" +
			(toBeUpdated and f"<strong>{update==-1 and 'Downgrade' or 'Upgrade'} To: </strong>{toBeUpdated} {latest or ''}"
			or not (toBeInstalled or toBeRemoved or toBeUpdated) and " "
			or f"<strong>To be {toBeRemoved and 'removed' or 'installed'}: </strong>{toBeInstalled or toBeRemoved} {toBeInstalled and latest or ''}"))
			

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
