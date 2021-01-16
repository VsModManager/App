from ModVersion import ModVersion
class VersionList():
	def __init__(self, data, latest, filelist):
		# self.data = data
		self.versions = {}
		self.installed = False
		self.versionList = []
		x = 0
		for key in data:
			self.versions[key] = ModVersion(data[key])
			self.versions[key].index = x
			x += 1
			if latest == key:
				self.versions[key].latest = True
				self.latest = self.versions[key]
			self.versionList.append(key)
		self.versionList.reverse()

		for key in self.versions:
			if self.versions[key].get('filename') in filelist:
				self.installed = self.versions[key]

	# def isLatest(self, version):
	# 	return version == self.latest

	def get(self, value, other=None):
		if value == "lastVersion":
			return self.latest
		if value == "VersionList":
			return self.versionList

	def getVersion(self, version):
		return self.versions[version]