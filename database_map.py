#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import sqlite3
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

app = QApplication(sys.argv)

db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('led-tool.db')
db.open()


leds_model = QSqlTableModel()
leds_model.setTable("leds")
leds_model.select()

manufacturers_model = QSqlTableModel()
manufacturers_model.setTable("manufacturers")
manufacturers_model.select()

families_model = QSqlTableModel()
families_model.setTable("families")
families_model.select()

def get_selection(selection):
    selected = lview.selectionModel().selectedIndexes()
    index = selection.indexes()
    if len(index) > 0:
        record = index[0].row()
        print(leds_model.record(record).value(1))

view = QTableView()
view.setModel(leds_model)
view.resize(1000, view.height());

lview = QListView()
lview.setModel(leds_model)
lview.setModelColumn(1)
a = lview.selectionModel().selectionChanged.connect(get_selection)

led_id = QLineEdit()

mapper = QDataWidgetMapper()
mapper.setModel(leds_model)
mapper.addMapping(led_id, 1)
mapper.toFirst()
mapper.setSubmitPolicy(QDataWidgetMapper.AutoSubmit)

box = QWidget()
box.resize(1200, box.height());
layout = QVBoxLayout()
layout.addWidget(view)
layout.addWidget(lview)
layout.addWidget(led_id)
box.setLayout(layout)

box.show()

app.exec_()
