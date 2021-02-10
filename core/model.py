import json
import pathlib
import os


class model:

	def __init__(self):
		self.isNew = 1
		self.primaryKey = 'id'
		self.sql = {}
		self._fields = {}
		self.model = {}
		self.select = []
		self.dirtyKey = []
		self.dirtyValue = []
		self.criteria = ''
		self.cachePath = pathlib.Path(f'core/cache/{self.table}.json')
		if not pathlib.Path('core/cache').is_dir():
			os.makedirs('core/cache')

	def process(self):
		if self.cachePath.is_file():
			model = json.loads(self.cachePath.read_text(encoding='utf-8'))
		else:
			cursor = self.manager.db.cursor()
			sql = f"PRAGMA table_info({self.table})"
			cursor.execute(sql)
			model = cursor.fetchall()
			modelJson = json.dumps(model)
			self.cachePath.write_text(modelJson, encoding='utf-8')
		for column in model:
			self.model[column[1]] = {
				'i': column[0],
				'name': column[1],
				'type': column[2],
			}
			self._fields[column[1]] = column[4]
			self.select.append(column[1])
		pass

	def criteria2where(self, criteria):
		txt = []
		for name in criteria:
			txt.append(f"`{name}` LIKE '{criteria[name]}'")
		if (len(txt) > 0):
			return " WHERE " + ' AND '.join(txt)
		else:
			return ''

	def initialize(self):
		cursor = self.manager.db.cursor()
		sql = f"SELECT {','.join(self.select)} FROM `{self.table}` {self.criteria};"
		cursor.execute(sql)
		row = cursor.fetchone()
		if row:
			for cell in range(len(row)):
				self._fields[self.select[cell]] = row[cell]
			self.isNew = -1

	def get(self, key):
		return self._fields[key]

	def set(self, key, value):
		if (self._fields[key] != value):
			self.dirtyKey.append("`" + key + "`")
			self.dirtyValue.append("'" + value + "'")
			self._fields[key] = value

	def save(self):
		if self.isNew > 0:
			cursor = self.manager.db.cursor()
			cursor.execute(
				f"INSERT INTO `{self.table}` ({','.join(self.dirtyKey)}) VALUES ({','.join(self.dirtyValue)});")
			self.criteria = self.criteria2where({self.primaryKey: cursor.lastrowid})
			self.manager.db.commit()
			self.initialize()
			pass
		else:
			if len(self.dirtyKey) > 0:
				if not self.primaryKey in self.dirtyKey:
					cursor = self.manager.db.cursor()
					upd = []
					for k, v in enumerate(self.dirtyKey):
						upd.append(f"{v} = {self.dirtyValue[k]}")
						sql = f"UPDATE `{self.table}` SET {','.join(upd)} WHERE `{self.primaryKey}` = '{self.get(self.primaryKey)}';"
						cursor.execute(sql)
						self.criteria = self.criteria2where({self.primaryKey: cursor.lastrowid})
						self.manager.db.commit()
						self.initialize()
			pass

	def toArray(self):
		return self._fields


pass
