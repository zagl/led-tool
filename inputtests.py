#!/opt/local/bin/python3.4
# -*- coding: utf-8 -*-

import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pprint import pprint
from lxml.html import document_fromstring

# Style
#MAIN_TITLE_FONT = ("Helvetica", 40, "bold")
#TITLE_FONT = ("Helvetica", 18, "bold")
#SURVEY_FONT = ("Helvetica", 14)
#BUTTON_FONT = ("Helvetica", 18)
#TINY_FONT = ("Helvetica", 10)
#TEXT_FONT = ("Helvetica", 16)



class Form(QMainWindow):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.setWindowTitle("LED Tool")

        tables = QWidget()
        table_layout = QHBoxLayout()
        tables.setLayout(table_layout)

        for i in range(0,5):
            self.table = QTableWidget(parent=self)
            self.table.setColumnCount(2)
            self.table.setRowCount(3)
            self.table.setHorizontalHeaderLabels(['current [A]','voltage [V]'])
            self.table.setItem(0,0,QTableWidgetItem('1e-5'))
            self.table.setItem(0,1,QTableWidgetItem('9.81'))
            self.table.setItem(1,0,QTableWidgetItem('5e4'))
            self.table.setItem(1,1,QTableWidgetItem('7.303'))
            self.table.horizontalHeader().setStretchLastSection(True)
            self.table.verticalHeader().hide()
            table_layout.addWidget(self.table)


        self.spinbox = QDoubleSpinBox(parent=self)
        self.spinbox.setSuffix(" mm")
        self.spinbox.setRange(0, 100000000)
        self.spinbox.setDecimals(5)

        self.edit = QLineEdit(parent=self)
        self.edit.setValidator( QDoubleValidator(0, 100, 2, self))

        layout = QVBoxLayout()
        layout.addWidget(tables)
        layout.addWidget(self.spinbox)
        layout.addWidget(self.edit)

        main_widget = QWidget()
        main_widget.setLayout(layout)

        self.setCentralWidget(main_widget)

        self.clip = QApplication.clipboard()

    def keyPressEvent(self, event):

        default = True

        if (event.modifiers() & Qt.ControlModifier):
            if event.key() == Qt.Key_C: #copy
                self.copyTableToClipboard()
                default = False

            if event.key() == Qt.Key_V: #paste
                self.pasteClipboardToTable()
                default = False

        if default:
            super(Form, self).keyPressEvent(event)

    def copyTableToClipboard(self):
        selected = self.table.selectedRanges()

        html = "<table>"
        text = ""

        for row_i in range(selected[0].topRow(), selected[0].bottomRow()+1):
            html += "<tr>"
            for column_i in range(selected[0].leftColumn(), selected[0].rightColumn()+1):
                html += "<td>"
                try:
                    content = self.table.item(row_i,column_i).text()
                    html += content
                    text += content
                except AttributeError:
                    pass

                html += "</td>"
                text += "\t"

            html += "</tr>"
            text += "\n"

        html += "</tr></table>"

        mime = QMimeData()
        mime.setHtml(html)
        mime.setText(text)
        self.clip.setMimeData(mime)

    def pasteClipboardToTable(self):
        mime = self.clip.mimeData()
        data = list()

        if mime.hasText():
            text = str(mime.text()).strip()
            rows = text.split("\n")
            for row in rows:
                row = row.strip()
                row_content = list()
                correct_entry = True
                for cell in row.split('\t'):
                    text = cell.strip()
                    if "," in text:
                        text = text.replace(",", '.')
                    try:
                        value = float(text)
                        row_content.append(value)
                    except ValueError:
                        correct_entry = False
                if correct_entry:
                    data.append(row_content)
            print(data)

class MyDoubleSpinBox(QDoubleSpinBox):

    def __init__(self, parent=None):
        super(MyDoubleSpinBox, self).__init__(parent)

        self.setMaximum(1e10)
        self.setMinimum(0.1)
        self.setDecimals(5)

    def textFromValue(self, value):
        return "%g" % value

class BrightnessGroupEditor(QWidget):

    def __init__(self, parent=None):
        super(BrightnessGroupEditor, self).__init__(parent)

        table = [
            ["AX", 2],
            ["CS", 3],
            ["BD", 4],
        ]

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Group','Luminous Flux [lm]'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().hide()

        for i, row in enumerate(table):
            self.table.insertRow(i)
            self.table.setItem(i,0,QTableWidgetItem(row[0]))
            self.table.setItem(i,1,QTableWidgetItem("{f:G}".format(f=row[1])))

        layout= QHBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

class VoltageGroupEditor(BrightnessGroupEditor):

    def __init__(self, parent=None):
        super(VoltageGroupEditor, self).__init__(parent)
        self.table.setHorizontalHeaderLabels(['Group','Voltage [V]'])

class GraphEditor(QWidget):

    def __init__(self, parent=None):
        super(GraphEditor, self).__init__(parent)

        table = [
            [1., 7e5],
            [2., 8e5],
            [3., 9e5],
            [4., 1e6],
            [5., 2e6],
        ]

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['current [mA]','voltage [V]'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().hide()

        for i, row in enumerate(table):
            self.table.insertRow(i)
            for j, cell in enumerate(row):
                self.table.setItem(i,j,QTableWidgetItem("{f:G}".format(f=cell)))

        layout= QHBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

class ParameterEditor(QWidget):

    def __init__(self, parent=None):
        super(ParameterEditor, self).__init__(parent)

        layout = QGridLayout()

        name_label = QLabel("Name:")
        layout.addWidget(name_label, 0, 0)
        name_edit = QLineEdit()
        layout.addWidget(name_edit, 0, 1)

        manufacturer_label = QLabel("Manufacturer:")
        layout.addWidget(manufacturer_label, 1, 0)
        manufacturer_combo = QComboBox()
        manufacturer_combo.setEditable(True)
        layout.addWidget(manufacturer_combo, 1, 1)
        self.setLayout(layout)

        family_label = QLabel("Family:")
        layout.addWidget(family_label, 2, 0)
        family_combo = QComboBox()
        family_combo.setEditable(True)
        layout.addWidget(family_combo, 2, 1)
        self.setLayout(layout)

        voltage_label = QLabel("Typical voltage:")
        layout.addWidget(voltage_label, 3, 0)
        voltage_edit = MyDoubleSpinBox()
        voltage_edit.setSuffix(" V")
        layout.addWidget(voltage_edit, 3, 1)

        current_label = QLabel("Typical current:")
        layout.addWidget(current_label, 4, 0)
        current_edit = MyDoubleSpinBox()
        current_edit.setSuffix(" mA")
        layout.addWidget(current_edit, 4, 1)

        resistance_label = QLabel("Thermal resistance J-B:")
        layout.addWidget(resistance_label, 5, 0)
        resistance_edit = MyDoubleSpinBox()
        resistance_edit.setSuffix(" K/W")
        layout.addWidget(resistance_edit, 5, 1)

        reference_temperature_label = QLabel("Reference temperature:")
        layout.addWidget(reference_temperature_label, 6, 0)
        reference_temperature_edit = MyDoubleSpinBox()
        reference_temperature_edit.setSuffix(" °C")
        layout.addWidget(reference_temperature_edit, 6, 1)

class LedEditor(QWidget):

    def __init__(self, parent=None):
        super(LedEditor, self).__init__(parent)

        layout = QVBoxLayout()

        content_container = QWidget()
        content_layout = QHBoxLayout()
        content_container.setLayout(content_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.pages = (
            ("Parameter", ParameterEditor()),
            ("Brightness Groups", BrightnessGroupEditor()),
            ("Voltage Groups", VoltageGroupEditor()),
#            ("spectrum",),
#            ("current vs. voltage",),
#            ("current vs. relative luminous flux",),
#            ("temperature vs. voltage",),
#            ("temperature vs. relative luminous flux",),
        )

        self.navigator = QListWidget()
        self.stack = QStackedWidget()
        for page in self.pages:
            self.navigator.addItem(page[0])
            self.stack.addWidget(page[1])

        content_layout.addWidget(self.navigator)
        content_layout.addWidget(self.stack)

        layout.addWidget(content_container)
        layout.addWidget(button_box)

        self.stack.setCurrentIndex(0)

        self.navigator.currentTextChanged.connect(self.changePage)

        self.setLayout(layout)

    def changePage(self):
        self.stack.setCurrentIndex(self.navigator.currentRow())


app = QApplication(sys.argv)

form = LedEditor()
form.show()
app.exec_()




