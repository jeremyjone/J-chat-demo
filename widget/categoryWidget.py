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


TEST_ITEM = [
    {
        "UserName": "Jz",
        "Avatar": "./Resource/image/Avatar/Jz.png",
        "Signature": u"你是我的小苹果",
        "ChatMessage": [
            {
                "Id": "j08q9234fh8q34f09wur34",
                "Date": "2019-5-1 12:20:36",
                "Message": u"你好",
            },
            {
                "Id": "jmwer098gfjh2q39804jhf",
                "Date": "2019-5-1 12:20:48",
                "Message": u"我知道",
            },
            {
                "Id": "jf092q34jf34jf834098ua",
                "Date": "2019-5-1 13:01:02",
                "Message": u"这是啥",
            },
            {
                "Id": "jf0983j98t23479u2340rd",
                "Date": "2019-5-1 14:05:40",
                "Message": u"埃及活动GIFUA贺岁发哈根达斯富奥斯卡吉利丁粉海菊沙发上发挥",
            },
        ]
    },
    {
        "UserName": "123",
        "Avatar": "./Resource/image/Avatar/123.png",
    },
    {
        "UserName": "aaa",
        "Avatar": "./Resource/image/Avatar/aaa.png",
    },
    {
        "UserName": "bbb",
        "Avatar": "./Resource/image/Avatar/bbb.png",
        "Signature": "Beautiful",
    },
    {
        "UserName": "ccc",
        "Avatar": "./Resource/image/Avatar/ccc.png",
    },
    {
        "UserName": "ddd",
        "Avatar": "./Resource/image/Avatar/ddd.png",
    },
    {
        "UserName": "eee",
        "Avatar": "./Resource/image/Avatar/eee.png",
    },
    {
        "UserName": "fff",
        "Avatar": "./Resource/image/Avatar/fff.png",
        "Signature": "Hello",
    },
    {
        "UserName": "ggg",
        "Avatar": "./Resource/image/Avatar/ggg.png",
    },
    {
        "UserName": "xyz",
        "Avatar": "./Resource/image/Avatar/xyz.png",
    },
]





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
        for item in TEST_ITEM:
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



