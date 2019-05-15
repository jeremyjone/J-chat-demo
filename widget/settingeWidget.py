# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "jeremyjone"
__datetime__ = "2019/5/7 18:20"
__all__ = ["SettingDialog"]

import os, sys
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
from collections import OrderedDict

from widget import UILoader
from config.conModel import CONFIG
from config.jzChat import JzChat
import widget


LABEL = OrderedDict([
    ("base", u"基本"),
    ("main", u"主界面"),
    ("state", u"状态"),
    ("chat", u"会话"),
    ("remind", u"提醒"),
    ("file", u"文件"),
    ("hotkey", u"热键"),
    ("other", u"其他")
])


class MenuLabel(QtGui.QLabel):
    itemClickSignal = QtCore.Signal(QtGui.QLabel)

    def __init__(self, text, parent=None):
        super(MenuLabel, self).__init__(text, parent)
        self.focusFlag = False
        self._key = None
        self.setFixedHeight(35)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setMargin(10)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, name):
        self._key = name

    def enterEvent(self, *args, **kwargs):
        self.setStyleSheet("QLabel {background-color: white};")

    def leaveEvent(self, *args, **kwargs):
        if self.focusFlag:
            return
        self.setStyleSheet("QLabel {};")

    def mousePressEvent(self, *args, **kwargs):
        self.setFocus()
        self.itemClickSignal.emit(self)

    def focusInEvent(self, event):
        self.focusFlag = True
        self.setStyleSheet("QLabel {background-color: white};")

    def focusOutEvent(self, event):
        self.focusFlag = False
        self.setStyleSheet("QLabel {};")



class SettingDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(SettingDialog, self).__init__(parent)
        self.scrollFlag = False
        self.initUI()

    def initUI(self):
        win = UILoader("./Resource/ui/settings.ui", "./Resource/css/settings.css")

        l = win.findChild(QtGui.QLayout, "gridLayout")
        self.setLayout(l)
        self.resize(win.width(), win.height())
        self.setStyleSheet(win.styleSheet())
        self.setFixedSize(self.width(), self.height())

        self.menuLabelLayout = self.findChild(QtGui.QLayout, "menuLabelLayout")

        for k, v in LABEL.items():
            label = MenuLabel(v, self)
            label.setObjectName("menu_label_" + k)
            label.key = k
            label.itemClickSignal.connect(self.onItemClicked)
            self.menuLabelLayout.addWidget(label)
        self.findChild(QtGui.QLabel, "menu_label_" + LABEL.keys()[0]).setFocus()  # init first label focus.

        self.scrollArea = self.findChild(QtGui.QScrollArea, "scrollArea")
        self.scrollArea.verticalScrollBar().valueChanged.connect(self.onValueChanged)

        ##### Add setting section.

        # Always on top
        AlwaysOnTop = self.findChild(QtGui.QCheckBox, "AlwaysOnTop")
        if CONFIG.Window.AlwaysOnTop:
            AlwaysOnTop.setCheckState(QtCore.Qt.Checked)
        else:
            AlwaysOnTop.setCheckState(QtCore.Qt.Unchecked)
        AlwaysOnTop.stateChanged.connect(
            lambda state: self.changeItemConfig(JzChat.settingWindow, AlwaysOnTop, state))

        # Close edge hide
        CloseEdgeHide = self.findChild(QtGui.QCheckBox, "CloseEdgeHide")
        if CONFIG.Window.CloseEdgeHide:
            CloseEdgeHide.setCheckState(QtCore.Qt.Checked)
        else:
            CloseEdgeHide.setCheckState(QtCore.Qt.Unchecked)
        CloseEdgeHide.stateChanged.connect(
            lambda state: self.changeItemConfig(JzChat.settingWindow, CloseEdgeHide, state))

        # Show in task bar
        ShowInTaskBar = self.findChild(QtGui.QCheckBox, "ShowInTaskBar")
        if CONFIG.Window.ShowInTaskBar:
            ShowInTaskBar.setCheckState(QtCore.Qt.Checked)
        else:
            ShowInTaskBar.setCheckState(QtCore.Qt.Unchecked)
        ShowInTaskBar.stateChanged.connect(
            lambda state: self.changeItemConfig(JzChat.settingWindow, ShowInTaskBar, state))

        # Show name on title
        ShowNameOnTitle = self.findChild(QtGui.QCheckBox, "ShowNameOnTitle")
        if CONFIG.Window.ShowNameOnTitle:
            ShowNameOnTitle.setCheckState(QtCore.Qt.Checked)
        else:
            ShowNameOnTitle.setCheckState(QtCore.Qt.Unchecked)
        ShowNameOnTitle.stateChanged.connect(
            lambda state: self.changeItemConfig(JzChat.settingWindow, ShowNameOnTitle, state))

        # Show minimize button on title bar.
        ShowMinimizeButton = self.findChild(QtGui.QCheckBox, "ShowMinimizeButton")
        if CONFIG.Window.ShowMinimizeButton:
            ShowMinimizeButton.setCheckState(QtCore.Qt.Checked)
        else:
            ShowMinimizeButton.setCheckState(QtCore.Qt.Unchecked)
        ShowMinimizeButton.stateChanged.connect(
            lambda state: self.changeItemConfig(JzChat.settingWindow, ShowMinimizeButton, state))

    def onValueChanged(self, value):
        if self.scrollFlag:
            return
        for k in LABEL.keys():
            widget = self.findChild(QtGui.QWidget, "widget_" + k)
            if widget and not widget.visibleRegion().isEmpty():
                label = self.findChild(QtGui.QLabel, "menu_label_" + k)
                label.setFocus()
                return

    def onItemClicked(self, Label):
        widget = self.findChild(QtGui.QWidget, "widget_" + Label.key)
        if not widget:
            return
        self.scrollFlag = True
        self.scrollArea.verticalScrollBar().setSliderPosition(widget.pos().y())
        self.scrollFlag = False

    def changeItemConfig(self, section, item, state):
        configName = item.objectName()
        CONFIG.setData(section, configName, state)

        # if configName == "AlwaysOnTop":
        #     widget.WIDGET.stayOnTop()
        #
        # if configName == "ShowInTaskBar":
        #     widget.WIDGET.showInTaskBar()

        if configName == "ShowNameOnTitle":
            widget.WIDGET.titleBar.setWindowTitle()

        if configName == 'ShowMinimizeButton':
            widget.WIDGET.titleBar.showMinButton()
