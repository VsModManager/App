import requests

class Mod():
	def __init__(self, data):
			self.data = data
			self.versions = []
			for key in self.data['versions']:
				if self.data['versions'][key]['version'] == self.data['lastVersion']:
					self.data['versions'][key]["latest"] = True
				else:
					self.data['versions'][key]["latest"] = False
				self.versions.append(self.data['versions'][key]['version'])
			self.versions.reverse()
			self.state = {"toInstall": False, "toDelete": False}

	# def __getattr__(self, name):
	# 	return self.get(name)

	def get(self, name, default=None):
		if name == "author":
			if self.data["authors"] == None or len(self.data["authors"]) == 0: return "Unknown"
			return self.data["authors"][0]
		if name == "authors":
			if self.data["authors"] == None or len(self.data["authors"]) == 0: return "Unknown"
			return ", ".join(self.data["authors"])

		if name in self.data and self.data[name] != None:
			return self.data[name]
		return default

	def getVersions(self, version = None):
		if not version is None: return self.data['versions'][version]
		return self.data['versions']

	def getLastVersion(self):
		return self.data['lastVersion']

	def render(self):
		installed = False
		name = self.data['name']
		author = self.formatString(self.get("author"), 14)
		downloads = self.data['downloads']
		version = self.getLastVersion()
		print(self.getVersions(version))
		gameVersion = self.getVersions(version)['gameVersion'] or "Unknown"
		id = self.data['id']
		return [installed, name, author, downloads, version, gameVersion, id]

	def formatString(self, string, limit):
		try:
			if len(string) > limit:
				return string[:limit]+'…'
			return string
		except:
			return 'Unknown'

	def download(self):
		url = self.getLastVersion()['downloadLink']
		request = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, allow_redirects=True)
		print(url, request.headers)
		# open
		# open('facebook.ico', 'wb').write(request.content)
