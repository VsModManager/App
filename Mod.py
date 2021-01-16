from VersionList import VersionList
from ModVersion import ModVersion

class Mod():
	def __init__(self, data, filelist):
			self.data = data
			self.data['versions'] = VersionList(self.data['versions'], self.data['lastVersion'], filelist)
			self.state = {"toInstall": False, "toDelete": False, "toUpdate": False, "installed": self.data['versions'].installed}
			self.versionList = self.data['versions']
			self.versions = self.versionList.get("VersionList")
			
	# def __getattr__(self, name):
	# 	return self.get(name)
	def __str__(self):
		return self.data['name']

	
	def get(self, name, other=None):
		if name in ["installed", "toInstall", "toDelete", "toUpdate"]:
			if isinstance(self.state[name], ModVersion):
				if other:
					return str(self.state[name])
				return self.state[name]
			return False


		if name == "author":
			if self.data["authors"] == None or len(self.data["authors"]) == 0: return "Unknown"
			return self.data["authors"][0]
		if name == "authors":
			if self.data["authors"] == None or len(self.data["authors"]) == 0: return "Unknown"
			return ", ".join(self.data["authors"])

		if name in self.data and self.data[name] != None:
			return self.data[name]
		return other

	def getVersion(self, version = None):
		if not version is None: return self.versionList.getVersion(version)
		return self.data['versions']

	def getLastVersion(self):
		return self.versionList.get('lastVersion')

	def render(self):
		installed = self.state['installed'] and True or False
		name = str(self)
		author = self.formatString(self.get("author"), 14)
		downloads = "Null" #self.data['downloads']
		version = str(self.getLastVersion())
		gameVersion = self.getVersion(version).get('gameVersion') or "Unknown"
		id = self.data['id']
		return [installed, name, author, downloads, version, gameVersion, id]

	def formatString(self, string, limit):
		try:
			if len(string) > limit:
				return string[:limit]+'…'
			return string
		except:
			return 'Unknown'

	# def download(self):
	# 	url = self.getLastVersion()['downloadLink']
	# 	request = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, allow_redirects=True)
	# 	print(url, request.headers)
		# open
		# open('facebook.ico', 'wb').write(request.content)
