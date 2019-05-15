# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "jeremyjone"
__datetime__ = "2019/5/7 22:20"
__all__ = ["GroupItem"]

import os, sys
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from widget import UILoader, circleAvatar


class GroupItem(QtGui.QDialog):
    def __init__(self, item, parent=None):
        super(GroupItem, self).__init__(parent)
        self._item = item
        self.initUI()
        self.setBackground()  # Set style.

        self.avatarLabel.setPixmap(circleAvatar(self.avatarLabel.width(),"./Resource/image/group_default.png"))

    def initUI(self):
        win = UILoader("./Resource/ui/groupItem.ui")

        l = win.findChild(QtGui.QLayout, "gridLayout")
        self.setLayout(l)
        self.resize(win.width(), win.height())
        self.setStyleSheet(win.styleSheet())

        self.groupItemWidget = self.findChild(QtGui.QWidget, "GroupItemWidget")
        self.avatarLabel = self.findChild(QtGui.QLabel, "avatar")
        self.groupNameLabel = self.findChild(QtGui.QLabel, "groupName")
        self.userListLabel = self.findChild(QtGui.QLabel, "userList")
        self.infoLabel = self.findChild(QtGui.QLabel, "groupInfo")
        self.dateLabel = self.findChild(QtGui.QLabel, "date")
        self.unreadLabel = self.findChild(QtGui.QLabel, "unreadLabel")

    def setBackground(self, flag=False):

        with open("./Resource/css/groupItem.css", 'r') as rf:
            css = rf.read()

        # Checked and unchecked styles.
        if flag:
            css += "#GroupItemWidget {background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(202, 202, 202, 255), stop:0.2 rgba(180, 180, 180, 255), stop:0.5 rgba(130, 130, 130, 255), stop:0.8 rgba(180, 180, 180, 255), stop:0.9 rgba(202, 202, 202, 222), stop:1 rgba(255, 255, 255, 150));}"
        else:
            css += "#GroupItemWidget {background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(222, 222, 222, 255), stop:0.2 rgba(200, 200, 200, 255), stop:0.5 rgba(150, 150, 150, 255), stop:0.8 rgba(200, 200, 200, 255), stop:0.9 rgba(222, 222, 222, 222), stop:1 rgba(255, 255, 255, 150));}"

        self.setStyleSheet(css)

    def mousePressEvent(self, *args, **kwargs):
        print "mousePressEvent"

    def mouseDoubleClickEvent(self, *args, **kwargs):
        print self.objectName()

    def enterEvent(self, *args, **kwargs):
        self.setBackground(True)

    def leaveEvent(self, *args, **kwargs):
        self.setBackground()