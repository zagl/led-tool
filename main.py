#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from  ui_main import Ui_MainWindow
from ledmodel import LedModel

class Delegate(QItemDelegate):
    def __init__(self, parent=None):
        super(Delegate, self).__init__(parent)
    
    def setEditorData(self, editor, index);
        pass


class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setupSignalsSlots()
        self.switchToMain()

        self.current_id = None

        self.led_model = LedModel()

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('led-tool.db')
        db.open()

        self.manufacturers_model = QSqlTableModel()
        self.manufacturers_model.setTable("manufacturers")
        self.manufacturers_model.select()

        self.ui.brightness_group_table_view.setModel(self.led_model)

        self.ui.manufacturer_combo.setModel(self.manufacturers_model)
        self.ui.manufacturer_combo.setModelColumn(1)

        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.led_model)
        self.mapper.addMapping(self.ui.name_edit, 1)
        self.mapper.addMapping(self.ui.typical_voltage_spin, 6)
        self.mapper.addMapping(self.ui.typical_current_spin, 7)
        self.mapper.addMapping(self.ui.thermal_resistance_spin, 4)
        self.mapper.addMapping(self.ui.reference_temperature_spin, 5)
        self.mapper.addMapping(self.ui.manufacturer_combo, 3)
        self.mapper.toFirst()

        self.ui.led_filter.installEventFilter(self)

        self.ui.main_stacked_widget.setCurrentIndex(1)
        self.ui.editor_stacked_widget.setCurrentIndex(0)

    def setupSignalsSlots(self):
        self.ui.edit_led_button.clicked.connect(self.switchToEditor)
        self.ui.buttonBox.clicked.connect(self.switchToMain)

    def switchToEditor(self):
        self.ui.main_stacked_widget.setCurrentIndex(1)

    def switchToMain(self):
        self.ui.main_stacked_widget.setCurrentIndex(0)

    def eventFilter(self, source, event):
        if source is self.ui.led_filter:
            if event.type() == QEvent.KeyPress:
                if event.key() == Qt.Key_Escape:
                    self.ui.led_filter.clear()
        return QWidget.eventFilter(self, source, event)

    def keyPressEvent(self, event):

        default = True

        if event.key() == Qt.Key_Escape:
            self.switchToMain()
            default = False
#        if (event.modifiers() & Qt.ControlModifier):
#            if event.key() == Qt.Key_C: #copy
#                self.copyTableToClipboard()
#                default = False
#
#            if event.key() == Qt.Key_V: #paste
#                self.pasteClipboardToTable()
#                default = False

        if default:
            super(Window, self).keyPressEvent(event)


app = QApplication(sys.argv)

window = Window()
window.show()
app.exec_()




