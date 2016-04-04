# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class LedModel(QAbstractTableModel):

    editCompleted = pyqtSignal(str)

    def __init__(self, parent=None):
        super(LedModel, self).__init__(parent)

        self.rows = 5
        self.cols = 2

        self.m_gridData = [[i*j for i in range(self.cols) ] for j in range(self.rows)]

    def rowCount(self, index):
        return self.rows

    def columnCount(self, index):
        return self.cols

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.m_gridData[index.row()][index.column()]

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            # save value from editor to member m_gridData
            self.m_gridData[index.row()][index.column()] = str(value)
            # for presentation purposes only: build and emit a joined string
            result = ''
            for row in range(self.rows):
                for col in range(self.cols):
                    result += self.m_gridData[row][col] + ' '
            self.editCompleted.emit(result)
        return True

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return 'first'
                elif section == 1:
                    return 'second'
                elif section == 2:
                    return 'third'

