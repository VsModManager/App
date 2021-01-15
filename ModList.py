from Mod import Mod
from taskScheduler import TaskScheduler
from time import sleep
import hashlib
import json
import requests
import numpy as np
from os.path import isfile

class ModList():
	def __init__(self, form, moddir, host, filename='modListData.json'):
		self.filename = filename
		progressBar = form.progressBar
		self.form = form
		self.TaskScheduler = TaskScheduler(self.form)
		self.host = host
		self.moddir = moddir
		sleep(0.1)
		progressBar.setValue(20)
		if (isfile(self.filename)):
			self.compareHash(progressBar)
		else:
			sleep(0.1)
			progressBar.setValue(40)
			self.updateModList()
			sleep(0.05)
			progressBar.setValue(60)
		self.mods = []
		sleep(0.1)
		progressBar.setValue(90)
		self.generateModList()
		sleep(0.05)
		progressBar.setValue(100)

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
				self.updateModList()
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

	def updateModList(self):
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
		for mod in self.rawData:
			self.mods.append(Mod(mod))

	def render(self):
		renderList = []
		for mod in self.mods:
			renderList.append(mod.render())
		return renderList

	def setMod(self, id):

		self.selectedMod = self.mods[id]
		self.form.comboBox.clear()
		self.form.comboBox.addItem("Latest")
		self.form.comboBox.addItems(self.selectedMod.versions)
		self.form.modName.setText(self.selectedMod.get('name', 'Unknown'))
		self.form.modDesc.setText(self.selectedMod.get('description', 'Unknown'))
		modInfo = ""
		modInfo += f"<strong>Author: </strong>{self.selectedMod.get('authors', 'Unknown')}<br>"
		modInfo += f"<strong>Downloads: </strong>{self.selectedMod.get('downloads', 'Unknown')}<br>"
		modInfo += f"<strong>Views: </strong>{self.selectedMod.get('views', 'Unknown')}<br>"
		self.form.modInfo.setText(modInfo)
		# self.form.<img src="">
		# Installed
		version = "0.0.0"
		latest = "" #self.selectedMod.data['versions'][version]["latest"] and "(Latest)" or ""
		if version != None:
			self.form.deleteText.setText(f"<strong>Installed: </strong>{version} {latest}")
	
			if version in self.selectedMod.versions:
				self.form.deleteButton.setEnabled(True)
			else:
				self.form.deleteButton.setEnabled(False)

		self.form.installButton.setEnabled(True)
		self.form.comboBox.setEnabled(True)


	def selectMod(self):
		select = self.form.comboBox.currentIndex()
		version = None
		if select == 0:
			version = self.selectedMod.data['lastVersion']
		else:
			version = self.selectedMod.data['versions'][self.selectedMod.versions[select-1]]
		return (self.selectedMod, version)


	def installMod(self):
		self.TaskScheduler.installMod(self.selectMod())
	def deleteMod(self):
		self.TaskScheduler.installMod(self.selectMod())
	def updateMod(self):
		self.TaskScheduler.installMod(self.selectMod())
	def applyMods(self):
		self.TaskScheduler.Apply()


	def downloadMod(self):
		self.selectedMod.download()
		pass