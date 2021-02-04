from PyQt5 import uic, QtCore,QtGui
from PyQt5.QtWidgets import QApplication, QHeaderView
from PyQt5.QtCore import Qt

class TableModel(QtCore.QAbstractTableModel):

		def __init__(self, List, data, header):
			super(TableModel, self).__init__()
			self.setNewData(data)
			# ['', 'Name', 'Author', 'Raiting', 'Downloads', 'Version', 'gameversion', '']
			self._header = header
			self._list = List
			self._search = {
				"text": ""
			}
			self._first = False
			self.icons = {
				"tick": QtGui.QIcon('tick.png'),
				"cross": QtGui.QIcon('cross.png')
			}
					# 	return QtGui.QIcon('tick.png')
					# return QtGui.QIcon('cross.png')

		def data(self, index, role):
			if role == Qt.DisplayRole:
				value = self._data[index.row()][index.column()]
				if isinstance(value, bool):
					return
				return str(value)

			if role == Qt.DecorationRole:
				value = self._data[index.row()][index.column()]
				
				if isinstance(value, bool):
					if value:
						return self.icons["tick"]
					return self.icons["cross"]

			if role == Qt.TextAlignmentRole:
				# value = self._data[index.row()][index.column()]
				if self._header[index.column()] == "Downloads":
					return Qt.AlignVCenter + Qt.AlignRight
				elif index.column() > 1:
					return Qt.AlignVCenter + Qt.AlignHCenter
				return Qt.AlignVCenter

		def rowCount(self, index):
			return len(self._data)

		def columnCount(self, index):
			return len(self._data[0])

		def headerData(self, section, orientation, role):
			# section is the index of the column/row.
			if role == Qt.DisplayRole:
				if orientation == Qt.Horizontal:
					if not self._first:
						self._first = True
						_header = self._list.horizontalHeader()
						for i, k in enumerate(self._header):
							if i == 1:
								_header.setSectionResizeMode(i, QHeaderView.Stretch)
							else:
								_header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
							if k == "" and i != 0:
								self._list.setColumnHidden(i, True)
					return str(self._header[section])

				# if orientation == Qt.Vertical:
				# 	return str(self._data.index[section])
		def setNewData(self, data):
			def sort(elem):
				return elem[1]
			self._data = sorted(data, key=sort)


		def setSearch(self, text):
			self._search["text"] = text.lower()
			self.filterData()

		def filterData(self):
			for k, e in enumerate(self._data):
				if e[1].lower().find(self._search["text"]) != -1 or e[2].lower().find(self._search["text"]) != -1:
					self._list.setRowHidden(k, False)
				else:
					self._list.setRowHidden(k, True)