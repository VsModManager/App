import os
import json
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication


class settingsManager():
	def __init__(self, form, dataPath, modDirPath):
		self.modListDataFile = dataPath + 'modListData.json'
		self.dataPath = dataPath
		self.modDirPath = modDirPath
		self.cacheDirPath = self.dataPath + "cache\\"
		self.imageDirPath = self.dataPath + "img\\"
		self.settingsFile = self.dataPath + "settings.json"
		self.form = form
		if not os.path.isdir(self.dataPath):
			os.mkdir(self.dataPath)
		if not os.path.isdir(self.imageDirPath):
			os.mkdir(self.imageDirPath)

		baseDict = {
			"disableCache": False,
			"saveCache": 30,
			"language": "en",
		}

		if os.path.exists(self.settingsFile):
			self.data = json.load(open(self.settingsFile, "r"))
			self.data = {**baseDict, **self.data}
			json.dump(self.data, open(self.settingsFile, 'w'))
		else:
			self.data = baseDict
			json.dump(self.data, open(self.settingsFile, 'w'))

		if not os.path.isdir(self.cacheDirPath):
			os.mkdir(self.cacheDirPath)
		self.form.disableCache.setChecked(self.data["disableCache"])
		self.form.cacheDays.setValue(self.data["saveCache"])

		def change_type():
			if self.form.cacheSizemultiplayer.text() == "MB":
				self.form.cacheSizemultiplayer.setText("GB")
			else:
				self.form.cacheSizemultiplayer.setText("MB")
		self.form.cacheSizemultiplayer.clicked.connect(change_type)

		def clearCache():
			for file in os.listdir(self.cacheDirPath):
				if os.path.isfile(self.cacheDirPath + file) and file.endswith('.zip'):
					os.remove(self.cacheDirPath + file)
		self.form.clearCache.clicked.connect(clearCache)

	def get(self, value):
		if value in ["disableCache", "saveCache", "language"]:
			return self.data[value]
		return getattr(self, value)

	def apply(self):
		self.data["disableCache"] = self.form.disableCache.isChecked()
		self.data["saveCache"] = self.form.cacheDays.value()
		json.dump(self.data, open(self.settingsFile, 'w'))
		pass

