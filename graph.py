#!/opt/local/bin/python3.4
# -*- coding: utf-8 -*-

import sys, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np

class Graph(QWidget):

    def __init__(self, parent=None):
        super(Graph, self).__init__(parent)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        self.view.setScene(self.scene)


        layout = QHBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.updateGraph()

    def resizeEvent(self, event):
        self.updateGraph()

    def updateGraph(self):
        self.scene.clear()

        width = self.view.size().width()
        height = self.view.size().height()

        border = 20

        draw_width = width - 2*border
        draw_height = height - 2*border

        data = np.array([ [i, pow(i,2)] for i in range(5) ])

        for point in data:
            self.scene.addEllipse(point[0], point[1], 1, 1)

        self.view.fitInView( self.scene.sceneRect(), Qt.KeepAspectRatio )




app = QApplication(sys.argv)

form = Graph()
form.show()
app.exec_()




