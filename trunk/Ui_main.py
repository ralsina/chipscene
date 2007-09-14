# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/centos/home/ralsina/Desktop/proyectos/pyweek5/twistedboy/lib/main.ui'
#
# Created: Thu Sep  6 11:24:15 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName("Main")
        Main.resize(QtCore.QSize(QtCore.QRect(0,0,593,578).size()).expandedTo(Main.minimumSizeHint()))

        self.widget = QtGui.QWidget(Main)
        self.widget.setGeometry(QtCore.QRect(9,9,570,561))
        self.widget.setObjectName("widget")

        self.vboxlayout = QtGui.QVBoxLayout(self.widget)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.play = QtGui.QToolButton(self.widget)
        self.play.setMinimumSize(QtCore.QSize(25,25))
        self.play.setIcon(QtGui.QIcon(":/icons/player_play.svg"))
        self.play.setCheckable(True)
        self.play.setChecked(False)
        self.play.setAutoExclusive(True)
        self.play.setObjectName("play")
        self.hboxlayout.addWidget(self.play)

        self.pause = QtGui.QToolButton(self.widget)
        self.pause.setMinimumSize(QtCore.QSize(25,25))
        self.pause.setIcon(QtGui.QIcon(":/icons/player_pause.svg"))
        self.pause.setCheckable(True)
        self.pause.setChecked(True)
        self.pause.setAutoExclusive(True)
        self.pause.setObjectName("pause")
        self.hboxlayout.addWidget(self.pause)

        self.line = QtGui.QFrame(self.widget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.hboxlayout.addWidget(self.line)

        spacerItem = QtGui.QSpacerItem(491,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.view = QtGui.QGraphicsView(self.widget)
        self.view.setObjectName("view")
        self.vboxlayout.addWidget(self.view)

        self.retranslateUi(Main)
        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        Main.setWindowTitle(QtGui.QApplication.translate("Main", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.play.setText(QtGui.QApplication.translate("Main", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.pause.setText(QtGui.QApplication.translate("Main", "...", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Main = QtGui.QDialog()
    ui = Ui_Main()
    ui.setupUi(Main)
    Main.show()
    sys.exit(app.exec_())
