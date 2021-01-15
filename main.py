
if __name__ == '__main__':
	# import hashlib
	# import json
	# import requests
	# import numpy as np
	import os
	from time import sleep


	import pandas as pd
	from PyQt5 import uic  # QtCore, QtGui
	from PyQt5.QtCore import QTimer
	from PyQt5.QtWidgets import QApplication, QHeaderView

	from ModList import ModList
	from TableModel import TableModel


	modDirPath = os.getenv('APPDATA')+r"\VintagestoryData\Mods"
	serverRequestUrl = "https://traineratwot.aytour.ru/vs/get/mods"

	# progress.config(mode = 'indeterminate')
	# progress.start()
	# progress.stop()

	# startUpForm, startUpWindow = uic.loadUiType("startup.ui")
	# startUpapp = QApplication([])
	# startUpwindow = startUpWindow()
	# startUpform = startUpForm()
	# startUpform.setupUi(startUpwindow)

	# startUpform.timer = QTimer()
	# startUpform.timer.start(1000)
	# startUpform.timer.timeout.connect(onStartup)
	# startUpwindow.show()
	# startUpapp.exec_()

	Form, Window = uic.loadUiType(".ui")
	app = QApplication([])
	window = Window()
	form = Form()
	form.setupUi(window)

	modList = None


	def onStartup():
		def modListClicked(selected, deselected):
			index = form.modList.model().index(selected.row(), 6)
			modList.setMod(int(index.data())-1)

		form.timer.stop()
		modList = ModList(form, modDirPath, serverRequestUrl)
		data = pd.DataFrame(modList.render(), columns = ['', 'Name', 'Author', 'Downloads', 'Version', 'gameversion', ''])
		# model = TableModel(data)
		# model.currentRowChanged(modListClicked)
		form.modList.setModel(TableModel(data))
		form.modList.selectionModel().currentRowChanged.connect(modListClicked)
		form.modList.selectRow(0)
		# form.modList.clicked.connect(modListClicked)
		form.installButton.clicked.connect(modList.installMod)
		form.deleteButton.clicked.connect(modList.deleteMod)
		form.updateButton.clicked.connect(modList.updateMod)
		form.applyButton.clicked.connect(modList.applyMods)
		form.progressBar.setValue(100)


		#style
		header = form.modList.horizontalHeader()
		header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
		header.setSectionResizeMode(1, QHeaderView.Stretch)
		header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
		header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
		header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
		header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
		header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
		form.modList.setColumnHidden(6, True)
		#styleEnd



	form.timer = QTimer()
	form.timer.start(300)
	form.timer.timeout.connect(onStartup)
	form.progressBar.setValue(10)
	# form.comboBox.setEnabled(True)
	# form.comboBox.addItem("Latest")
	# form.comboBox.addItems(["0.0.0"])


	#style
	form.modDesc.setStyleSheet("background-color: #F0F0F0;")
	modInfo = f"<strong>Author: <strong><br>"
	modInfo += f"<strong>Downloads: <strong><br>"
	modInfo += f"<strong>Views: <strong><br>"
	form.modInfo.setText(modInfo)
	#styleEnd


	window.show()
	app.exec_()
