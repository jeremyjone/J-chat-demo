# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Enumeration class of a program.
"""
__author__ = "jeremyjone"
__datetime__ = "2019/5/10 22:26"
__all__ = ["JzChat"]


class JzChat:
    ChatMessageSend = 1
    ChatMessageRecv = 2
    Left = 101
    Top = 102
    Right = 103
    LeftTop = 104
    RightTop = 105
    LeftBottom = 106
    RightBottom = 107
    Bottom = 108


    ChatTextHeight = 35
    ChatMessageMargin = 8
    ChatMessageRadius = 15
    ChatMessageTriangleWidth = 8

    settingWindow = "Window"

    UserItemHover = "{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(210, 210, 210, 255), stop:0.2 rgba(200, 200, 200, 255), stop:0.5 rgba(182, 182, 182, 255), stop:0.8 rgba(192, 192, 192, 255), stop:0.9 rgba(210, 210, 210, 222), stop:1 rgba(255, 255, 255, 150));}"
    UserItemNormal = "{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(240, 240, 240, 255), stop:0.2 rgba(230, 230, 230, 255), stop:0.5 rgba(212, 212, 212, 255), stop:0.8 rgba(222, 222, 222, 255), stop:0.9 rgba(240, 240, 240, 222), stop:1 rgba(255, 255, 255, 150));}"

    GroupItemHover = "{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(210, 210, 210, 255), stop:0.2 rgba(200, 200, 200, 255), stop:0.5 rgba(182, 182, 182, 255), stop:0.8 rgba(192, 192, 192, 255), stop:0.9 rgba(210, 210, 210, 222), stop:1 rgba(255, 255, 255, 150));}"
    GroupItemNormal = "{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(240, 240, 240, 255), stop:0.2 rgba(230, 230, 230, 255), stop:0.5 rgba(212, 212, 212, 255), stop:0.8 rgba(222, 222, 222, 255), stop:0.9 rgba(240, 240, 240, 222), stop:1 rgba(255, 255, 255, 150));}"
