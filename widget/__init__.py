# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "jeremyjone"
__datetime__ = "2019/4/30 18:02"
__all__ = ["UILoader", "circleAvatar"]

import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
from PySide import QtXml
from PySide.QtUiTools import QUiLoader


WIDGET = None



def UILoader(UI_File, css_name=None):
    '''Load UI file'''
    loader = QUiLoader()
    ui_file = QtCore.QFile(UI_File)
    ui_file.open(QtCore.QFile.ReadOnly)
    window = loader.load(ui_file)
    ui_file.close()
    if css_name:
        with open(css_name, 'r') as css_file:
            style_sheet = css_file.read()
        window.setStyleSheet(style_sheet)
    return window



def circleAvatar(width, picture):
    radius = width / 2
    target = QtGui.QPixmap(QtCore.QSize(width, width))
    target.fill(QtCore.Qt.transparent)

    # Loads the image and scales it as large as the control.
    p = QtGui.QPixmap(picture).scaled(width, width,
        QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)

    painter = QtGui.QPainter(target)

    # anti-aliasing.
    painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
    painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
    painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)

    path = QtGui.QPainterPath()
    path.addRoundedRect(
        0, 0, width, width, radius, radius)
    # rounded.
    painter.setClipPath(path)

    painter.drawPixmap(0, 0, p)
    return target