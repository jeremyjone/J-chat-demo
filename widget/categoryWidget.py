# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Category item, it is mainly used to classify users.
It can customize styles and properties.
"""
__author__ = "jeremyjone"
__datetime__ = "2019/5/5 21:32"
__all__ = ["CategoryItem"]

import os, sys
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from widget import UILoader
from widget.userItemWidget import UserItem
from config.conModel import CONFIG


class CategoryItem(QtGui.QWidget):
    def __init__(self, categoryName, parent=None):
        super(CategoryItem, self).__init__(parent)
        self._animationTime = CONFIG.Window.CategoryAnimationTime
        self._animationValid = CONFIG.Window.CategoryAnimationValid
        self._height = None
        self.initUI()

        self.setCategoryName(categoryName)
        self.setExpandBtnIcon()
        self.addUserItem()

        self._topMargins = self.categoryLayout.getContentsMargins()[1]
        self._bottomMargins = self.categoryLayout.getContentsMargins()[3]

    def initUI(self):
        win = UILoader("./Resource/ui/category.ui", "./Resource/css/category.css")

        l = win.findChild(QtGui.QLayout, "gridLayout")
        self.setLayout(l)
        self.resize(win.width(), win.height())
        self.setStyleSheet(win.styleSheet())

        self.categoryWidget = self.findChild(QtGui.QWidget, "categoryWidget")
        self.categoryLabel = self.findChild(QtGui.QLabel, "categoryLabel")
        self.categoryLayout = self.findChild(QtGui.QLayout, "categoryLayout")

        self._verticalWidget = self.findChild(QtGui.QWidget, "verticalWidget")
        self.userLayout = self.findChild(QtGui.QLayout, "UserLayout")
        self.expandBtn = self.findChild(QtGui.QPushButton, "expandBtn")
        self.expandBtn.clicked.connect(self.expandHandle)

    def setCategoryName(self, name):
        self.categoryLabel.setText(name)

    def addUserItem(self):
        for item in range(10):
            userItem = UserItem(item)
            self.userLayout.addWidget(userItem)

    def expandHandle(self):
        self.ani = QtCore.QPropertyAnimation(self.categoryWidget, b"geometry")
        self.ani.setDuration(self._animationTime)

        if self._verticalWidget.isVisible():
            # Save user item widget height
            if self._animationValid:
                self._height = self.height()
                self.ani.setStartValue(QtCore.QRect(self.categoryWidget.x(), self.categoryWidget.y(), self.categoryWidget.width(), self._height - self.categoryLabel.height() - self._topMargins - self._bottomMargins))
                self.ani.setEndValue(QtCore.QRect(self.categoryWidget.x(), self.categoryWidget.y(), self.categoryWidget.width(), self.categoryLabel.height()))
                self.ani.start()
                self.ani.finished.connect(self.widgetHide)
            else:
                self._verticalWidget.hide()
        else:
            if self._animationValid:
                self.ani.setStartValue(QtCore.QRect(self.categoryWidget.x(), self.categoryWidget.y(), self.categoryWidget.width(), self.categoryLabel.height()))
                self.ani.setEndValue(QtCore.QRect(self.categoryWidget.x(), self.categoryWidget.y(), self.categoryWidget.width(), self._height))
                self.ani.start()
            self._verticalWidget.show()

        self.setExpandBtnIcon(self._verticalWidget.isVisible())

    def widgetHide(self):
        self._verticalWidget.hide()
        self.setExpandBtnIcon(False)

    def setExpandBtnIcon(self, expand=True):
        icon = QtGui.QIcon()

        if expand:
            icon.addPixmap(QtGui.QPixmap("./Resource/icon/expandRight.png"))
        else:
            icon.addPixmap(QtGui.QPixmap("./Resource/icon/expandBottom.png"))

        self.expandBtn.setIcon(icon)
        self.expandBtn.setIconSize(QtCore.QSize(16, 16))



