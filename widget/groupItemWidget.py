# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "jeremyjone"
__datetime__ = "2019/5/7 22:20"
__all__ = ["GroupItem"]

import os, sys
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from widget import UILoader, circleAvatar
from config.jzChat import JzChat


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
            css += "#GroupItemWidget %s" % JzChat.GroupItemHover
        else:
            css += "#GroupItemWidget %s" % JzChat.GroupItemNormal

        self.setStyleSheet(css)

    def mousePressEvent(self, *args, **kwargs):
        print "mousePressEvent"

    def mouseDoubleClickEvent(self, *args, **kwargs):
        print self.objectName()

    def enterEvent(self, *args, **kwargs):
        self.setBackground(True)

    def leaveEvent(self, *args, **kwargs):
        self.setBackground()