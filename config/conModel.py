# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
All configure information of this software.
Every config section has default value, and all config section
will try to load the personalization configuration each time.
"""
__author__ = "jeremyjone"
__datetime__ = "2019/5/7 14:01"
__all__ = ["LoadConfig", "CONFIG"]

import os

import config


_ConfigurationInfo = """
[Main]
Name = JzChat

[Window]
Width = 250
Height = 650
AlwaysOnTop = 0
ShowInTaskBar = 1
CloseEdgeHide = 1
HideAnimationTime = 200
CategoryAnimationTime = 100
CategoryAnimationValid = 1
TabAnimationTime = 100
TabAnimationValid = 1
ShowNameOnTitle = 1
ShowMinimizeButton = 1
CloseButtonExit = 0

[State]

[Chat]
SendColor = #499C54
RecvColor = #C1B929
TextColor = #0F0F0F
AlwaysShowName = 0

[Other]

"""


class __MAIN:
    pass


class __WINDOW:
    pass


class __STATE:
    pass


class __CHAT:
    pass


class __OTHER:
    pass


_MAIN = __MAIN()
_WINDOW = __WINDOW()
_STATE = __STATE()
_CHAT = __CHAT()
_OTHER = __OTHER()


class LoadConfig(object):
    def __init__(self):
        # mainPath = os.path.expanduser("~/JzChat")
        mainPath = "."
        filename = "JzChatConfig.ini"

        configFile = os.path.join(mainPath, filename)

        if not os.path.exists(configFile):
            if not os.path.exists(mainPath):
                os.mkdir(mainPath)
            with open(configFile, "w") as wf:
                wf.write(_ConfigurationInfo)

        self._config = config.JConfig(configFile)

        self.__getData()

    def __getData(self):
        # Add Main section
        self.Main.Name = self._config.getConfig("Main", "Name")

        # Add Window section
        self.Window.Width = int(self._config.getConfig("Window", "Width"))
        self.Window.Height = int(self._config.getConfig("Window", "Height"))
        self.Window.AlwaysOnTop = int(self._config.getConfig("Window", "AlwaysOnTop"))
        self.Window.CloseEdgeHide = int(self._config.getConfig("Window", "CloseEdgeHide"))
        self.Window.ShowInTaskBar = int(self._config.getConfig("Window", "ShowInTaskBar"))
        self.Window.HideAnimationTime = int(self._config.getConfig("Window", "HideAnimationTime"))
        self.Window.CategoryAnimationTime = int(self._config.getConfig("Window", "CategoryAnimationTime"))
        self.Window.CategoryAnimationValid = int(self._config.getConfig("Window", "CategoryAnimationValid"))
        self.Window.TabAnimationTime = int(self._config.getConfig("Window", "TabAnimationTime"))
        self.Window.TabAnimationValid = int(self._config.getConfig("Window", "TabAnimationValid"))
        self.Window.ShowNameOnTitle = int(self._config.getConfig("Window", "ShowNameOnTitle"))
        self.Window.ShowMinimizeButton = int(self._config.getConfig("Window", "ShowMinimizeButton"))
        self.Window.CloseButtonExit = int(self._config.getConfig("Window", "CloseButtonExit"))

        # Add Chat section
        self.Chat.SendColor = (self._config.getConfig("Chat", "SendColor"))
        self.Chat.RecvColor = (self._config.getConfig("Chat", "RecvColor"))
        self.Chat.TextColor = (self._config.getConfig("Chat", "TextColor"))
        self.Chat.AlwaysShowName = int(self._config.getConfig("Chat", "AlwaysShowName"))

    def setData(self, section, key, value):
        setattr(self.__getattribute__(section), key, value)
        self._config.setConfig(section, key, str(value))

    @property
    def Main(self):
        return _MAIN

    @property
    def Window(self):
        return _WINDOW

    @property
    def State(self):
        return _STATE

    @property
    def Chat(self):
        return _CHAT

    @property
    def Other(self):
        return _OTHER


CONFIG = LoadConfig()
