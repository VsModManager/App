import json
import os


class settingsManager:
	def __init__(self, form, cache, dataPath, modDirPath):
		self.modListDataFile = dataPath + 'modListData.json'
		self.dataPath = dataPath
		self.cache = cache
		self.modDirPath = modDirPath
		self.cacheDirPath = self.dataPath + "cache\\"
		self.cache.setCachePath(self.cacheDirPath)
		self.cache.setSettings(self)
		self.imageDirPath = self.dataPath + "img\\"
		self.settingsFile = self.dataPath + "settings.json"
		self.form = form
		if not os.path.isdir(self.dataPath):
			os.makedirs(self.dataPath)
		if not os.path.isdir(self.imageDirPath):
			os.makedirs(self.imageDirPath)

		baseDict = {
				"disableCache": False,
				"saveCache": 30,
				"language": "en",
			}

		if os.path.exists(self.settingsFile):
			self.data = json.load(open(self.settingsFile, "r"))
			self.data = baseDict | self.data
			json.dump(self.data, open(self.settingsFile, 'w'))
		else:
			self.data = baseDict
			json.dump(self.data, open(self.settingsFile, 'w'))

		if not os.path.isdir(self.cacheDirPath):
			os.makedirs(self.cacheDirPath)
		self.form.disableCache.setChecked(self.data["disableCache"])
		self.form.cacheDays.setValue(self.data["saveCache"])

		def change_type():
			if self.form.cacheSizemultiplayer.text() == "MB":
				self.form.cacheSizemultiplayer.setText("GB")
			else:
				self.form.cacheSizemultiplayer.setText("MB")
		self.form.cacheSizemultiplayer.clicked.connect(change_type)



	def __call__(self, value):
		return self.get(value)

	def get(self, value):
		if value in ["disableCache", "saveCache", "language"]:
			return self.data[value]
		return getattr(self, value)

	def apply(self):
		self.data["disableCache"] = self.form.disableCache.isChecked()
		self.data["saveCache"] = self.form.cacheDays.value()
		json.dump(self.data, open(self.settingsFile, 'w'))

