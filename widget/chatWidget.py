# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Chat Window, P2P chat only show text part,
P2G chat will show person list in group.
"""
__author__ = "jeremyjone"
__datetime__ = "2019/5/9 20:32"
__all__ = ["ChatWidget"]

import os, sys
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from widget import UILoader, circleAvatar
from config.jzChat import JzChat
from config.conModel import CONFIG


ITEM = [
    {
        "Username": "Jeremyjone",
        "Text": u"韩国发哦ID烦恼斯蒂芬大家噶速度开了房间爱上了快递费哈根哈地方哈迪斯饭局的算法第三方韩国发哦ID烦恼斯蒂芬大家噶速度开了房间爱上了快递费哈根哈地方哈迪斯饭局的算法第三方爱上了快递费哈根哈地方哈迪斯饭局的算法第三方",
        "Type": JzChat.ChatMessageSend
    },

    {
        "Username": "Jeremyjone",
        "Text": u"afgas gadfa sdgwtu fasdfjpo ajw eg upgndl jfakdsj fkas djnfv aosdn voaismvas dfasdfas dgasdfa sfasf",
        "Type": JzChat.ChatMessageRecv
    },

    {
        "Username": "Jeremyjone",
        "Text": u"你好！",
        "Type": JzChat.ChatMessageRecv
    },
    {
        "Username": "Jeremyjone",
        "Text": u"你好！",
        "Type": JzChat.ChatMessageRecv
    },
    {
        "Username": "Jeremyjone",
        "Text": u"你好！",
        "Type": JzChat.ChatMessageRecv
    },
    {
        "Username": "Jeremyjone",
        "Text": u"你好！",
        "Type": JzChat.ChatMessageSend
    },
    {
        "Username": "Jeremyjone",
        "Text": u"你好啊啊啊你好啊啊啊你好啊啊啊",
        "Type": JzChat.ChatMessageRecv
    },
    {
        "Username": "Jeremyjone",
        "Text": u"我",
        "Type": JzChat.ChatMessageSend
    }
]



class ChatTextLabel(QtGui.QLabel):
    def __init__(self, item, parent=None):
        super(ChatTextLabel, self).__init__(parent)
        self._item = item
        self.messageMargin = JzChat.ChatMessageMargin

        self.setWordWrap(True)
        self.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse | QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.ClipOperation)
        self.setContentsMargins(self.messageMargin, self.messageMargin,
                                self.messageMargin, self.messageMargin)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        # First, the text is loaded, the Label size is supported,
        # and then the text is processed transparently.
        self.setText(item["Text"])
        _style = "border-radius: %dpx;" % JzChat.ChatMessageRadius

        if self._item["Type"] == JzChat.ChatMessageSend:
            self.setAlignment(QtCore.Qt.AlignTop)
            _style += "background-color: %s" % CONFIG.Chat.SendColor
        elif self._item["Type"] == JzChat.ChatMessageRecv:
            self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
            _style += "background-color: %s" % CONFIG.Chat.RecvColor

        self.setStyleSheet(_style)

    # def paintEvent(self, event):
    #     super(ChatTextLabel, self).paintEvent(event)
    #     _text = self._item["Text"]
    #     _metrics = QtGui.QFontMetrics(self.font())
    #     bound = _metrics.boundingRect(0, 0, self.width(), self.height(), QtCore.Qt.TextWordWrap | QtCore.Qt.AlignLeft,
    #                                   _text)
    #
    #     if self.width() > bound.width() + self.messageMargin * 2:
    #         self.resize(bound.width() + self.messageMargin * 2, self.height())


class TriangleLabel(QtGui.QLabel):
    def __init__(self, type, parent=None):
        super(TriangleLabel, self).__init__(parent)
        self.type = type

    def paintEvent(self, event):
        super(TriangleLabel, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        triPath = QtGui.QPainterPath()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)  # anti-aliasing

        # paint triangle
        if self.type == JzChat.ChatMessageSend:
            triPath.moveTo(0, JzChat.ChatMessageRadius + 2)
            triPath.lineTo(JzChat.ChatMessageTriangleWidth, JzChat.ChatMessageRadius)
            triPath.lineTo(0, JzChat.ChatMessageRadius + 10)
            backColor = CONFIG.Chat.SendColor
        elif self.type == JzChat.ChatMessageRecv:
            triPath.moveTo(JzChat.ChatMessageTriangleWidth, JzChat.ChatMessageRadius + 2)
            triPath.lineTo(0, JzChat.ChatMessageRadius)
            triPath.lineTo(JzChat.ChatMessageTriangleWidth, JzChat.ChatMessageRadius + 10)
            backColor = CONFIG.Chat.RecvColor

        # Brush background
        painter.setBrush(QtGui.QColor(backColor))
        # Draw rect and triangle
        painter.setPen(QtGui.QColor(backColor))
        painter.drawPath(triPath)


class ChatTextWidget(QtGui.QWidget):
    def __init__(self, item, parent=None):
        super(ChatTextWidget, self).__init__(parent)
        self._item = item
        self.initUI()

    def initUI(self):
        win = UILoader("./Resource/ui/textLine.ui")

        l = win.findChild(QtGui.QLayout, "gridLayout")
        self.setLayout(l)
        self.resize(win.width(), win.height())
        self.setStyleSheet(win.styleSheet())

        self.messageWidget = self.findChild(QtGui.QWidget, "messageWidget")
        self.avatarLabel = self.findChild(QtGui.QLabel, "avatarLabel")
        self.groupAvatarSpacer = self.findChild(QtGui.QWidget, "groupAvatarSpacer")

        # Show text widget, vertical layout, top is username label, bottom is text label.
        # When P2P chat window, username label is hidden.
        self.textLabel = ChatTextLabel(self._item, self)

        self.usernameLabel = QtGui.QLabel()
        self.usernameLabel.setObjectName("UsernameLabel")
        self.usernameLabel.setText(self._item["Username"])
        self.usernameLabel.setIndent(JzChat.ChatMessageMargin)

        self.textWidget = QtGui.QWidget()
        textLayout = QtGui.QVBoxLayout(spacing=2)
        textLayout.setContentsMargins(0, 0, 0, 0)
        self.textWidget.setLayout(textLayout)

        self.textRectWidget = QtGui.QWidget()
        textRectLayout = QtGui.QHBoxLayout(spacing=0)
        textRectLayout.setContentsMargins(0, 0, 0, 0)

        self.textRectWidget.setLayout(textRectLayout)

        if self.parent().isGroup or CONFIG.Chat.AlwaysShowName:
            textLayout.addWidget(self.usernameLabel)
        else:
            # P2P and not show name, avatar move up 5px.
            self.groupAvatarSpacer.hide()

        self.textRectWidget.layout().addWidget(self.textLabel)
        textLayout.addWidget(self.textRectWidget)

        self.triangleLabel = TriangleLabel(self._item["Type"])
        self.triangleLabel.setFixedWidth(JzChat.ChatMessageTriangleWidth)

        placeLabel = QtGui.QLabel()
        placeLabel.setFixedWidth(35 + 35)

        if self._item["Type"] == JzChat.ChatMessageSend:
            self.messageWidget.layout().setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.usernameLabel.setAlignment(QtCore.Qt.AlignRight)
            self.avatarLabel.setPixmap(circleAvatar(35, "./Resource/image/avatar.png"))

            self.textRectWidget.layout().addWidget(self.triangleLabel)
            self.messageWidget.layout().insertWidget(0, self.textWidget)  # Put text label to left.
            self.messageWidget.layout().insertSpacerItem(0, QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding))
            self.messageWidget.layout().insertWidget(0, placeLabel)
        if self._item["Type"] == JzChat.ChatMessageRecv:
            self.messageWidget.layout().setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            self.avatarLabel.setPixmap(circleAvatar(35, "./Resource/image/tiger.png"))

            self.textRectWidget.layout().insertWidget(0, self.triangleLabel)
            self.messageWidget.layout().addWidget(self.textWidget)
            self.messageWidget.layout().addSpacerItem(QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.MinimumExpanding,
                                                                              QtGui.QSizePolicy.Expanding))
            self.messageWidget.layout().addWidget(placeLabel)


class ChatWidget(QtGui.QWidget):
    def __init__(self, item, parent=None):
        super(ChatWidget, self).__init__(parent)
        self._item = item
        self.isGroup = self.item["isGroup"]
        # self.isGroup = True  # Group test switch.
        self.initUI()
        self.addTextWidget()

        self.show()

    def initUI(self):
        win = UILoader("./Resource/ui/chat.ui", "./Resource/css/chat.css")

        l = win.findChild(QtGui.QLayout, "gridLayout")
        self.setLayout(l)
        self.resize(win.width(), win.height())
        self.setStyleSheet(win.styleSheet())
        self.setWindowTitle("Chat with %s" % self._item["Username"])

        self.personScrollArea = self.findChild(QtGui.QWidget, "personWidget")
        if not self.isGroup:  # If not group chat widget, hide person list.
            self.personScrollArea.hide()
            self.resize(win.width() - 150, win.height())

        self.plainTextEdit = self.findChild(QtGui.QPlainTextEdit, "plainTextEdit")
        self.msgScrollArea = self.findChild(QtGui.QScrollArea, "msgScrollArea")

        self.sendBtn = self.findChild(QtGui.QPushButton, "sendBtn")

    @property
    def item(self):
        return self._item

    def addTextWidget(self):
        _userWrapWidget = QtGui.QWidget(self)
        # Lateral stretch, longitudinal fixation.
        # _userWrapWidget.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        listBox = QtGui.QVBoxLayout(spacing=10)
        listBox.setContentsMargins(0, 0, 0, 0)
        listBox.setAlignment(QtCore.Qt.AlignBottom)
        _userWrapWidget.setLayout(listBox)

        # Test data.
        for i in ITEM:
            listBox.addWidget(ChatTextWidget(i, self))

        self.msgScrollArea.setWidget(_userWrapWidget)

        # Made vertical scrollbar always stay bottom.
        self.msgScrollArea.verticalScrollBar().setSliderPosition(self.msgScrollArea.verticalScrollBar().maximum())


