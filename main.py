#!/opt/local/bin/python3.4
# -*- coding: utf-8 -*-

import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pprint import pprint
from lxml.html import document_fromstring

# Style
MAIN_TITLE_FONT = ("Helvetica", 40, "bold")
TITLE_FONT = ("Helvetica", 18, "bold")
SURVEY_FONT = ("Helvetica", 14)
BUTTON_FONT = ("Helvetica", 18)
TINY_FONT = ("Helvetica", 10)
TEXT_FONT = ("Helvetica", 16)


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.setWindowTitle("LED Tool")

        self.table = QTableWidget(parent=self)
        self.table.setColumnCount(2)
        self.table.setRowCount(3)
        self.table.setHorizontalHeaderLabels(['current [A]','voltage [V]'])
#        self.table.setVerticalHeaderLabels(['row1','row2'])
        self.table.setItem(0,0,QTableWidgetItem('foo'))
        self.table.setItem(0,1,QTableWidgetItem('bar'))
        self.table.setItem(1,0,QTableWidgetItem('baz'))
        self.table.setItem(1,1,QTableWidgetItem('qux'))

        layout = QHBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

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

        for row_i in xrange(selected[0].topRow(), selected[0].bottomRow()+1):
            html += "<tr>"
            for column_i in xrange(selected[0].leftColumn(), selected[0].rightColumn()+1):
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
        if mime.hasHtml():
            html = str(mime.html())
            page = document_fromstring(html)
            rows = page.xpath("body/table")[0].findall("tr")
            for row in rows:
                row_content = list()
                correct_entry = True
                for cell in row.getchildren():
                    text = cell.text_content()
                    if "," in text:
                        text = text.replace(",", '.')
                    value = -9999
                    try:
                        value = float(text)
                    except ValueError:
                        correct_entry = False
                    row_content.append(value)
                if correct_entry:
                    data.append(row_content)

        elif mime.hasText():
            text = str(mime.text())
            rows = text.split("\n")
            for row in rows:
                row_content = list()
                correct_entry = True
                for cell in row.split('\t'):
                    text = cell
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

app = QApplication(sys.argv)

form = Form()
form.show()
app.exec_()




