if __name__ == '__main__':
	# import hashlib
	# import json
	# import requests
	# import numpy as np
	import os
	import asyncio

	from PyQt5 import uic, QtGui  # QtCore, QtGui
	from PyQt5.QtCore import QTimer
	from PyQt5.QtWidgets import QApplication
	from settings import settingsManager
	from cacheController import cacheController
	# import Poedit

	from ModList import ModList
	# import logging
	import requests
	requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

	# os.remove('example.log')
	# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.WARN)
	# logging.captureWarnings(True)

	modDirPath = os.getenv('APPDATA') + "\\VintagestoryData\\Mods\\"
	serverRequestUrl = "https://vs.aytour.ru/vs/get/mods"
	updateCheckUrl = "https://archive.aytour.ru/vs/app/check"
	version = "0.1.1"
	versionId = 3

	dataPath = os.getenv('APPDATA') + "\\VintagestoryModManagerData\\"

	# lang = Poedit.lang('f7712fd43da0c33880d64b13d3352784', 407521)
	# lang.cachePath = dataPath + '\\lang\\'
	# lang.initialize()

	Form, Window = uic.loadUiType(".ui")
	app = QApplication([])
	window = Window()
	window.setWindowIcon(QtGui.QIcon('logo.ico'))
	form = Form()
	form.setupUi(window)

	cache = cacheController(form)
	settings = settingsManager(form, cache, dataPath, modDirPath, versionId)
	settings.version = [version, versionId]
	modList = None

	def onStartup():
		form.timer.stop()
		global modList
		modList = ModList(form, settings, serverRequestUrl)

		def textChanged():
			modList.TableModel.setSearch(form.searchBox.text())
		cache.setSize()

		form.searchBox.textChanged.connect(textChanged)
		form.comboBox.currentTextChanged.connect(modList.renderButtons)
		form.installButton.clicked.connect(modList.installMod)
		form.deleteButton.clicked.connect(modList.deleteMod)
		form.updateButton.clicked.connect(modList.updateMod)
		form.applyButton.clicked.connect(modList.applyMods)
		form.settingsApply.clicked.connect(settings.apply)
		form.tabWidget.setEnabled(True)
		form.progressBar.setValue(100)

	# style

	# form.modList.setColumnHidden(3, True)
	# styleEnd

	# form.actionSettings.triggered.connect(settings.openSettingsWindow)
	form.tabWidget.setEnabled(False)

	form.timer = QTimer()
	form.timer.start(300)
	form.timer.timeout.connect(onStartup)
	form.progressBar.setValue(10)
	def openSite():
		os.system(f'start https://vs.aytour.ru/')
	form.uploadmods.clicked.connect(openSite)

	def openCache():
		os.system(f'start {settings.cacheDirPath}')
	form.cacheFolder.clicked.connect(openCache)

	def openDownload():
		os.system(f'start https://vs.aytour.ru/download')
	form.newVersion.clicked.connect(openDownload)

	async def versionCheck():
		form.newVersion.setText(version)
		form.versionInfo.setText("Version: " + version)
		try:
			response = requests.request("GET", updateCheckUrl, verify=False)
			if response.ok:
				v = response.text
				if not settings.local:
					settings.local = False
				if versionId < int(v.split(":")[1]):
					form.newVersion.setText("New Version Available")
					form.newVersion.setStyleSheet("background-color: #FF1010;")
					form.newVersion.setEnabled(True)
					form.versionInfo.setText("Version: " + version + "<br>New version: " + v.split(":")[0])
			else:
				settings.local = True
		except:
			settings.local = True
			
	asyncio.run(versionCheck())

	# style
	style = "background-color: #E0E0E0;"
	style2 = "background-color: #F0F0F0;"
	form.modDesc.setStyleSheet(style)
	form.modInfo.setStyleSheet(style)
	form.color.setStyleSheet(style)
	form.color2.setStyleSheet(style2)
	# styleEnd

	window.show()
	# x = True
	# x = False
	# if x:
	# 	import pstats
	# 	from pstats import SortKey
	# 	import cProfile
	# 	cProfile.run('app.exec_()', 'restats')
	# 	pstats.Stats('restats').strip_dirs().sort_stats("cumtime").print_stats(20)
	# 	sleep(3)
	# else:
	app.exec_()

	cache.cleanCache()
