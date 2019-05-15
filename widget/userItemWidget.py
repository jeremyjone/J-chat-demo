# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
User item, each item is a user object.
It can customize styles and properties.
"""
__author__ = "jeremyjone"
__datetime__ = "2019/5/2 18:32"
__all__ = ["UserItem"]

import os, sys
import re
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from widget import UILoader, circleAvatar
from widget.chatWidget import ChatWidget
from config.jzChat import JzChat


class UserItem(QtGui.QWidget):
    def __init__(self, item, parent=None):
        super(UserItem, self).__init__(parent)
        self._item = item
        self.chatWindow = None

        win = UILoader("./Resource/ui/userItem.ui")

        l = win.findChild(QtGui.QLayout, "gridLayout")
        self.setLayout(l)
        self.resize(win.width(), win.height())
        self.setStyleSheet(win.styleSheet())

        self.userItemWidget = self.findChild(QtGui.QWidget, "UserItemWidget")
        self.avatarLabel = self.findChild(QtGui.QLabel, "avatar")
        self.usernameLabel = self.findChild(QtGui.QLabel, "username")
        self.infoLabel = self.findChild(QtGui.QLabel, "userInfo")
        self.dateLabel = self.findChild(QtGui.QLabel, "date")
        self.unreadLabel = self.findChild(QtGui.QLabel, "unreadLabel")

        self.setBackground()  # Set style.

        if os.path.exists(self._item.get("Avatar")):
            self.avatarLabel.setPixmap(circleAvatar(self.avatarLabel.width(), self._item["Avatar"]))
        else:
            self.avatarLabel.setPixmap(circleAvatar(self.avatarLabel.width(), "./Resource/image/Avatar/default.png"))

        self.usernameLabel.setText(self._item["UserName"])

        if self._item.get("Signature"):
            self.infoLabel.setText(self._item["Signature"])
        else:
            self.infoLabel.setText("")

        if self._item.get("ChatMessage"):
            if self._item["ChatMessage"][-1].get("Date"):
                dateText = re.findall(r"\d\d\d\d-(\d{1,2}-\d{1,2})", self._item["ChatMessage"][-1].get("Date"))
                if len(dateText) > 0:
                    self.dateLabel.setText(dateText[-1])
                self.unreadLabel.setText(str(len(self._item["ChatMessage"])))
        else:
            self.dateLabel.hide()
            self.unreadLabel.hide()

    def setBackground(self, flag=False):

        with open("./Resource/css/userItem.css", 'r') as rf:
            css = rf.read()

        # Checked and unchecked styles.
        if flag:
            css += "#UserItemWidget %s" % JzChat.UserItemHover
        else:
            css += "#UserItemWidget %s" % JzChat.UserItemNormal

        self.setStyleSheet(css)

    def createMenu(self):
        userMenu = QtGui.QMenu(self)
        chatMenu = userMenu.addAction("Chat Now")
        chatMenu.triggered.connect(self.openChatWindow)

        test = userMenu.addAction("test")
        test.triggered.connect(self.testHandle)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(
            lambda: userMenu.exec_(QtGui.QCursor.pos()))

    def testHandle(self):
        print self.chatWindow

    def openChatWindow(self):
        item = {
            "Username": self._item["UserName"],
            "isGroup": False,
        }
        self.chatWindow = ChatWidget(item, self)

    def mousePressEvent(self, event):
        # print dir(event)
        if event.button() == QtCore.Qt.RightButton:  # right button call menu
            self.createMenu()

    def mouseDoubleClickEvent(self, *args, **kwargs):
        self.openChatWindow()

    def enterEvent(self, *args, **kwargs):
        self.setBackground(True)

    def leaveEvent(self, *args, **kwargs):
        self.setBackground()


