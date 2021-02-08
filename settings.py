import json
import os
import shutil


class settingsManager:
	def __init__(self, form, cache, dataPath, modDirPath, versionId):
		self.modListDataFile = dataPath + 'modListData.json'
		self.dataPath = dataPath
		self.cache = cache
		self.local = False
		self.modDirPath = modDirPath
		self.cacheDirPath = self.dataPath + "cache\\"
		self.cache.setCachePath(self.cacheDirPath)
		self.cache.setSettings(self)
		self.imageDirPath = self.cacheDirPath + "img\\"
		self.settingsFile = self.dataPath + "settings.json"
		self.form = form
		if not os.path.isdir(self.dataPath):
			os.makedirs(self.dataPath)
		if not os.path.isdir(self.imageDirPath):
			os.makedirs(self.imageDirPath)

		baseDict = {
				"disableCache": False,
				"saveCache": 30,
				"cacheLimit": 0,
				"cacheLimitUnit": "MB",
				"localPics": True,
				"language": "en",
				"lastVersion": versionId
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
		self.form.localPics.setChecked(self.data["localPics"])
		self.form.cacheDays.setValue(self.data["saveCache"])
		self.form.cacheSizeLimit.setValue(self("cacheLimitRaw"))

		if self("cacheLimitUnit") in ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]:
			self.form.cacheSizemultiplayer.setText(self("cacheLimitUnit"))
		else:
			self.form.cacheSizemultiplayer.setText("MB")
			self.apply()

		def change_type():
			if self.form.cacheSizemultiplayer.text() == "MB":
				self.form.cacheSizemultiplayer.setText("GB")
			else:
				self.form.cacheSizemultiplayer.setText("MB")
		self.form.cacheSizemultiplayer.clicked.connect(change_type)
		
		if self("lastVersion") < versionId:
			self.migrate(self("lastVersion"), versionId)

	def migrate(self, version, versionId):
		if version <= 3:
			if os.path.isdir(self.dataPath + "img\\"):
				try:
					shutil.rmtree(self.dataPath + "img\\")
				except:
					pass
		self.apply(versionId)

	def __call__(self, value):
		return self.get(value)

	def get(self, value):
		if value == "cacheLimit":
			values = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
			return (1024**values.index(self("cacheLimitUnit")))*self("cacheLimitRaw")

		if value == "cacheLimitRaw": value = "cacheLimit"
		if value in ["disableCache", "saveCache", "cacheLimit", "cacheLimitUnit", "language", "localPics", "lastVersion"]:
			return self.data[value]
		return getattr(self, value)

	def apply(self, version=False):
		self.data["disableCache"] = self.form.disableCache.isChecked()
		self.data["saveCache"] = self.form.cacheDays.value()
		self.data["cacheLimit"] = self.form.cacheSizeLimit.value()
		self.data["cacheLimitUnit"] = self.form.cacheSizemultiplayer.text()
		self.data["localPics"] = self.form.localPics.isChecked()
		self.data["lastVersion"] = version or self.version[1]
		json.dump(self.data, open(self.settingsFile, 'w'))

