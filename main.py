#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from  ui_main import Ui_MainWindow
from ledmodel import LedModel

class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setupSignalsSlots()
        self.switchToMain()

        self.current_id = None

        self.led_model = LedModel()
        self.ui.brightness_group_table_view.setModel(self.led_model)

        self.ui.led_filter.installEventFilter(self)

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




