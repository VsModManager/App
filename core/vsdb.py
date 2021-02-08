import os
import sqlite3
import importlib


class manager:
	def __init__(self, path):
		if not os.path.isdir(path):
			os.makedirs(path)
		self.db = sqlite3.connect(path + 'data.db')

	def createBd(self):
		cursor = self.db.cursor()
		sqlVersion = """
		CREATE TABLE version (
			id           INTEGER       PRIMARY KEY AUTOINCREMENT,
			mod                        REFERENCES mod (id),
			version      VARCHAR (50),
			filename     VARCHAR (100),
			gameVersion  VARCHAR (50),
			modinfo      TEXT,
			changelog    TEXT,
			dependencies TEXT,
			date_create  BIGINT (20),
			CONSTRAINT UniqVer UNIQUE (
				mod,
				version
			)
			ON CONFLICT IGNORE
		);
		"""
		sqlMod = """
		CREATE TABLE mod (
			id          INTEGER       PRIMARY KEY AUTOINCREMENT,
			name        VARCHAR (100),
			modId       VARCHAR (100) UNIQUE,
			authors     TEXT,
			img         TEXT,
			gallery     TEXT,
			homepage    TIME,
			source      TEXT,
			side        VARCHAR (10)  DEFAULT both,
			published   BOOLEAN (1)   DEFAULT (0),
			tags        TEXT,
			lastVersion VARCHAR (30),
			downloads   BIGINT        DEFAULT (0),
			raiting     TEXT
		);
		"""
		pass

	def getObject(self, name, criteria=None):
		moduleName, dot, className = name.rpartition('.')
		module = importlib.import_module(moduleName)
		klass = getattr(module, className)
		_ = klass(self, criteria)
		if criteria:
			if not _.isNew:
				return False
		return _
		pass
