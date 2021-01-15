from PyQt5 import uic, QtCore,QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import pandas as pd
import numpy as np

class TableModel(QtCore.QAbstractTableModel):

		def __init__(self, data):
			super(TableModel, self).__init__()
			self._data = data

		def data(self, index, role):
			if role == Qt.DisplayRole:
				value = self._data.iloc[index.row(), index.column()]
				if isinstance(value, np.bool_):
					return
				return str(value)

			if role == Qt.DecorationRole:
				value = self._data.iloc[index.row(), index.column()]
				
				if isinstance(value, np.bool_):
					if value:
						return QtGui.QIcon('tick.png')
					return QtGui.QIcon('cross.png')

		def rowCount(self, index):
			return self._data.shape[0]

		def columnCount(self, index):
			return self._data.shape[1]

		def headerData(self, section, orientation, role):
			# section is the index of the column/row.
			if role == Qt.DisplayRole:
				if orientation == Qt.Horizontal:
					return str(self._data.columns[section])

				if orientation == Qt.Vertical:
					return str(self._data.index[section])