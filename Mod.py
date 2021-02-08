from VersionList import VersionList
from ModVersion import ModVersion

import re


class Mod:
	def __init__(self, data, filelist, local=False):
		self.data = data
		self.data['versions'] = VersionList(self.data['versions'], self.data['lastVersion'], filelist)
		self.state = {"toInstall": False, "toDelete": False, "toUpdate": False,
					  "installed": self.data['versions'].installed}
		self.versionList = self.data['versions']
		self.versions = self.versionList.get("VersionList")

	# def __getattr__(self, name):
	# 	return self.get(name)
	def __str__(self):
		return self.data['name']
	def __call__(self, value, other=None):
		return self.get(value)
	def get(self, name, other=None):
		if name in ["installed", "toInstall", "toDelete", "toUpdate"]:
			if isinstance(self.state[name], ModVersion):
				if other:
					return str(self.state[name])
				return self.state[name]
			return False

		if name == "raiting":
			if self.data["raiting"]:
				if self.data["raiting"]["rating"]:
					return self.data["raiting"]["rating"] + "%"
			if other == True:
				return False
			return "Unknown%"

		if name == "tags":
			return ", ".join(self.data["tags"])
		if name == "img":
			if self.data["img"]:
				return self.data["img"]
			else:
				return False
		if name == "shotDescription":
			if self.data["descriptions"][other] != None: return self.data["descriptions"][other]['shotDescription']
			return self.data["descriptions"]['en']['shotDescription']
		if name == "description":
			regex = r"(<img)(.*?)(\>)"
			desc = ""
			subst = "[images is not yet supported]"
			if self.data["descriptions"][other] != None:
				desc = self.data["descriptions"][other]['description']
			else:
				desc = self.data["descriptions"]['en']['description']
			return re.sub(regex, subst, desc, flags = re.MULTILINE)
			
		if name == "author":
			if self.data["authors"] == None or len(self.data["authors"]) == 0: return "Unknown"
			return self.data["authors"][0]
		if name == "authors":
			if self.data["authors"] == None or len(self.data["authors"]) == 0: return "Unknown"
			return ", ".join(self.data["authors"])
		if name == "versionsToCombo":
			v = []
			for version in self.versions:
				v.append(f"[{self.versionList.getVersion(version)('gameVersion')}] {version}")
			return v
		if name in self.data and self.data[name] != None:
			return self.data[name]
		return other

	def hasFile(self, name):
		if name in self.versionList.get("allFiles"):
			return True
		return False

	def getVersion(self, version=None):
		if not version is None: return self.versionList.getVersion(version)
		return self.data['versions']

	def getLastVersion(self):
		return self.versionList.get('lastVersion')

	def render(self):
		state = ""
		if self.state["installed"]:
			# state = True
			state += "I"
			if self.state["installed"] != self.getLastVersion():
				state += "U"
		if self.state["toUpdate"]:
			state += "E"
		if self.state["toInstall"]:
			state += "+"
		if self.state["toDelete"]:
			state += "-"
		name = str(self)
		author = self.formatString(self.get("author"), 14)
		downloads = self.data['downloads'] or "----"
		version = str(self.getLastVersion())
		gameVersion = self.getVersion(version).get('gameVersion') or "Unknown"
		raiting = self.get("raiting", True) or "--.--%"
		id = self.data['id']
		return [state, name, author, raiting, downloads, version, gameVersion, id]

	def formatString(self, string, limit):
		try:
			if len(string) > limit:
				return string[:limit] + '…'
			return string
		except:
			return 'Unknown'

# def download(self):
# 	url = self.getLastVersion()['downloadLink']
# 	request = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, allow_redirects=True)
# 	print(url, request.headers)
# open
# open('facebook.ico', 'wb').write(request.content)
