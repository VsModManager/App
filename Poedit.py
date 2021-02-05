import json
import os
from pathlib import Path

import requests


class lang:
	def __init__(self, token, projectId):
		self.projectId = projectId
		self.lang = 'en'
		self.token = token
		self.url = 'https://api.poeditor.com/v2/'
		self.cachePath = f"lang/"
		self.filename = f"{self.lang}.json"
		self.dict = {}
		pass

	def __call__(self, key):
		return self._(key)
		pass

	def _(self, key):
		return self.dict[key]
		pass

	def initialize(self):
		if not os.path.isdir(self.cachePath):
			os.makedirs(self.cachePath)
		self.cachePath = Path(self.cachePath + self.filename)
		if self.cachePath.is_file():
			self.dict = json.loads(self.cachePath.read_text(), encoding='utf-8')
			pass
		else:
			self.createCache()
			pass

	def createCache(self):
		raw = self.listTerms()
		for term in raw['result']['terms']:
			self.dict[term['term']] = term['translation']['content']
		self.cachePath.write_text(json.dumps(self.dict))

	def setLang(self, lang):
		self.lang = lang

	def set(self, name, value):
		self[name] = value
		return True

	def get(self, name):
		return self[name]

	def listProjects(self):
		return self.curl('projects/list')

	def listTerms(self, id='', language=''):
		id = id or self.projectId
		language = language or self.lang
		return self.curl('terms/list', {'id': id, 'language': language});

	def curl(self, method, POST={}):
		try:
			data = dict({
				'api_token': self.token
			}, **POST)
			url = f'{self.url}{method}'
			headers = {}
			response = requests.request(method="POST", url=url, headers=headers, data=data, verify=False)
			return response.json()
		except:
			return False
