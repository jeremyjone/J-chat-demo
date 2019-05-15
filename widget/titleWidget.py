# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Window's custom title bar.
"""
__author__ = "jeremyjone"
__datetime__ = "2019/4/30 18:08"
__all__ = ["TitleWidget"]

import os, sys
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from widget import UILoader
from config.conModel import CONFIG


class TitleWidget(QtGui.QWidget):
    windowMinimumed = QtCore.Signal()
    # windowMaximumed = QtCore.Signal()
    # windowNormaled = QtCore.Signal()
    windowClosed = QtCore.Signal()
    windowMoved = QtCore.Signal(QtCore.QPoint)
    windowReleased = QtCore.Signal()

    def __init__(self, parent=None):
        super(TitleWidget, self).__init__(parent)
        self.mPos = None
        self.initUI()

    def initUI(self):
        win = UILoader("./Resource/ui/title.ui", "./Resource/css/title.css")

        l = win.findChild(QtGui.QLayout, "gridLayout")
        self.setLayout(l)
        self.setStyleSheet(win.styleSheet())
        self.setFixedHeight(win.height())

        self.APPNameLabel = self.findChild(QtGui.QLabel, "APPNameLabel")
        self.titleTextLabel = self.findChild(QtGui.QLabel, "titleTextLabel")
        self.setWindowTitle()

        iconLabel = self.findChild(QtGui.QLabel, "iconLabel")
        iconLabel.setPixmap(QtGui.QPixmap("./Resource/icon/ffm_main.png"))

        self.titleWidget = self.findChild(QtGui.QWidget, "titleWidget")
        # _palette = QtGui.QPalette()
        # _pixmap = QtGui.QPixmap("./Resource/image/background_title_2.png").scaled(
        #     self.titleWidget.width(), self.titleWidget.height(),
        #     QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        # _palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(_pixmap))
        # self.titleWidget.setPalette(_palette)

        self.minWinBtn = self.findChild(QtGui.QPushButton, "minWinBtn")
        self.minWinBtn.setToolTip(u"最小化")
        self.closeWinBtn = self.findChild(QtGui.QPushButton, "closeWinBtn")
        self.minWinBtn.clicked.connect(lambda : self.windowMinimumed.emit())

        self.showMinButton()

        if CONFIG.Window.CloseButtonExit:
            self.closeWinBtn.clicked.connect(lambda: sys.exit(0))
            self.closeWinBtn.setToolTip(u"退出")
        else:
            self.closeWinBtn.clicked.connect(lambda: self.windowClosed.emit())
            self.closeWinBtn.setToolTip(u"关闭窗口")

    def setWindowTitle(self, *args, **kwargs):
        if CONFIG.Window.ShowNameOnTitle:
            self.APPNameLabel.setText(CONFIG.Main.Name)
            self.titleTextLabel.setText(" - " + "Jz")
        else:
            self.APPNameLabel.setText("")
            self.titleTextLabel.setText("")

    def showMinButton(self):
        if not CONFIG.Window.ShowMinimizeButton:
            self.minWinBtn.hide()
        else:
            self.minWinBtn.show()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mPos = event.pos()
            event.accept()
            # It cannot be moved when the window is maximized or full screen.
            self._canMove = not self.isMaximized() or not self.isFullScreen()

    def mouseReleaseEvent(self, event):
        self.mPos = None
        event.accept()
        self._canMove = False
        self.windowReleased.emit()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self.mPos and self._canMove:
            self.windowMoved.emit(self.mapToGlobal(event.pos() - self.mPos))
            event.accept()

    def enterEvent(self, event):
        self.setCursor(QtCore.Qt.ArrowCursor)
        super(TitleWidget, self).enterEvent(event)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    t = TitleWidget()
    t.show()
    sys.exit(app.exec_())
