import os
import datetime
import math

def convert_size(size_bytes):
	if size_bytes == 0:
		return "0B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	if s > 10:
		s = round(size_bytes / p, 1)
	if s > 100 or s % 1 == 0:
		s = round(s)
	if s == 1024:
		s /= 1024
		s = round(s)
		i += 1
	return "%s %s" % (s, size_name[i])


class cacheController:
	def __init__(self, form):
		self.form = form
		self.form.clearCache.clicked.connect(self.clearCache)

	def setCachePath(self, path):
		self.cachePath = path
	def setSettings(self, settings):
		self.settings = settings

	def __call__(self, value):
		return self.get(value)

	def get(self, value):
		if value == "totalSize":
			return self.getSize()
		if value == "totalSizeB":
			return convert_size(self.getSize())
		return getattr(self, value)

	def getSize(self):
		totalSize = 0
		for file in os.listdir(self.cachePath):
			if os.path.isfile(self.cachePath + file) and file.endswith('.zip'):
				totalSize += os.stat(self.cachePath + file).st_size
		return totalSize
	def setSize(self):
		self.form.cacheSize.setText(self("totalSizeB"))



	def clearCache(self, ignore=False):
		for file in os.listdir(self.cachePath):
			if os.path.isfile(self.cachePath + file) and file.endswith('.zip'):
				os.remove(self.cachePath + file)
		if not ignore:
			self.setSize()
	def cleanCache(self):
		if self.settings.get("saveCache") != 0:
			for file in os.listdir(self.cachePath):
				if os.path.isfile(self.cachePath + file) and file.endswith('.zip'):
					if datetime.datetime.fromtimestamp(
							os.stat(self.cachePath + file).st_atime) + datetime.timedelta(
							days=self.settings.get("saveCache")) < datetime.datetime.now():
						os.remove(self.cachePath + file)
			
		self.cleanBySize()

	def cleanImages(self):
		if not settings("localPics"):
			for file in os.listdir(settings.imageDirPath):
				if os.path.isfile(settings.imageDirPath + file) and file.startswith('m'):
					os.remove(settings.imageDirPath + file)
		else:
			for file in os.listdir(settings.imageDirPath):
				if os.path.isfile(settings.imageDirPath + file) and file.startswith('m'):
					if datetime.datetime.fromtimestamp(os.stat(self.cachePath + file).st_atime) + datetime.timedelta(
							days=5) < datetime.datetime.now():
						os.remove(settings.imageDirPath + file)
	def cleanBySize(self):
		if self.settings("cacheLimitRaw") != 0:
			totalSize = self.getSize()
			if self.settings("cacheLimit") < totalSize:
				files = []
				for file in os.listdir(self.cachePath):
					if os.path.isfile(self.cachePath + file) and file.endswith('.zip'):
						files.append((file, os.stat(self.cachePath + file).st_atime, os.stat(self.cachePath + file).st_size))
				def _sort(file):
					return file[1]
				files.sort(key=_sort)
				i = 0
				while self.settings("cacheLimit") < totalSize:
					os.remove(self.cachePath + files[i][0])
					totalSize -= files[i][2]
					i+=1
