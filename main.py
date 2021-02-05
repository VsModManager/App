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

	from ModList import ModList
	# import logging
	import requests

	# os.remove('example.log')
	# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.WARN)
	# logging.captureWarnings(True)

	modDirPath = os.getenv('APPDATA') + "\\VintagestoryData\\Mods\\"
	serverRequestUrl = "https://vs.aytour.ru/vs/get/mods"
	updateCheckUrl = "https://archive.aytour.ru/vs/app/check"
	version = "0.1.0-rc1"
	versionId = 1

	dataPath = os.getenv('APPDATA') + "\\VintagestoryModManagerData\\"

	Form, Window = uic.loadUiType(".ui")
	app = QApplication([])
	window = Window()
	window.setWindowIcon(QtGui.QIcon('logo.ico'))
	form = Form()
	form.setupUi(window)

	settings = settingsManager(form, dataPath, modDirPath)
	modList = None


	def onStartup():
		form.timer.stop()
		global modList
		modList = ModList(form, settings, serverRequestUrl)

		def textChanged():
			modList.TableModel.setSearch(form.searchBox.text())

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


	# form.comboBox.setEnabled(True)
	# form.comboBox.addItem("Latest")
	# form.comboBox.addItems(["0.0.0"])
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
		response = requests.request("GET", updateCheckUrl, verify=False)
		if response.ok:
			if versionId >= int(response.text.split(":")[1]):
				form.newVersion.setText(version)
			else:
				form.newVersion.setText("New Version Available")
				form.newVersion.setEnabled(True)


	asyncio.run(versionCheck())

	# style
	style = "background-color: #E0E0E0;"
	form.modDesc.setStyleSheet(style)
	form.modInfo.setStyleSheet(style)
	form.color.setStyleSheet(style)
	form.color2.setStyleSheet(style)
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

	modList.clearCache()
	for file in os.listdir(settings.imageDirPath):
		if os.path.isfile(settings.imageDirPath + file) and file.startswith('m'):
			os.remove(settings.imageDirPath + file)
