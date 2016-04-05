# -*- coding: utf-8 -*-

import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sqlite3

class LedModel(QAbstractTableModel):

    editCompleted = pyqtSignal(str)

    def __init__(self, parent=None):
        super(LedModel, self).__init__(parent)

        filename = "led-tool.db"
        new = not os.path.exists(filename)
        self.conn = sqlite3.connect(filename)
        self.c = self.conn.cursor()

        self.rows = 0
        self.cols = 8

        self.columns = [
                "id",
                "name",
                "family",
                "manufacturer",
                "thermal_resistance_jb",
                "reference_temperature",
                "typical_voltage",
                "typical_current"
        ]

        query = """
            SELECT
                leds.id,
                leds.name,
                leds.family,
                leds.manufacturer,
                leds.thermal_resistance_jb,
                leds.reference_temperature,
                leds.typical_voltage,
                leds.typical_current
            FROM leds;
        """

        self.m_gridData = []

        for row in self.c.execute(query):
            self.m_gridData.append(list(row))
            self.rows += 1

    def rowCount(self, index):
        return self.rows

    def columnCount(self, index):
        return self.cols

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.m_gridData[index.row()][index.column()]

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled

    def setData(self, index, value, role):
        row = index.row()
        col = index.column()
        if role == Qt.EditRole:
            if col == 0 or col == 2 or col == 3:
                self.m_gridData[row][col] = int(value)
            elif col == 4 or col == 5 or col == 6 or col == 7:
                self.m_gridData[row][col] = float(value)
            elif col == 1:
                self.m_gridData[row][col] = str(value)
            self.c.execute("UPDATE leds SET {}=? WHERE id=?".format(self.columns[col]),
                (value, self.m_gridData[row][0] ))
            self.conn.commit()
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

