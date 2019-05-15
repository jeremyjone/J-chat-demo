# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Main interface style and data processing functions.
"""
__author__ = "jeremyjone"
__datetime__ = "2019/4/30 17:23"
__all__ = ["FramelessWidget", "MainPanel"]

import os, sys
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore

from config.conModel import CONFIG
from config.jzChat import JzChat
from widget import UILoader, circleAvatar
from widget.titleWidget import TitleWidget
from widget.userItemWidget import UserItem
from widget.groupItemWidget import GroupItem
from widget.categoryWidget import CategoryItem
from widget.settingeWidget import SettingDialog
import widget



class FramelessWidget(QtGui.QWidget):
    Margins = 5

    def __init__(self, parent=None):
        super(FramelessWidget, self).__init__(parent)
        self._pressed = False
        self.Direction = None
        self._ani_finish = True
        self._AnimationTime = CONFIG.Window.HideAnimationTime  # Animation duration, milliseconds.

        # Window's W & H, width is total screen width.
        self._win_width = QtGui.QApplication.desktop().screen().width()
        self._win_height = QtGui.QApplication.desktop().availableGeometry(self).height()

        self._mainLayout = QtGui.QVBoxLayout(spacing=0)
        self._mainLayout.setContentsMargins(self.Margins, self.Margins, self.Margins, self.Margins)
        self.setLayout(self._mainLayout)
        self.resize(CONFIG.Window.Width, CONFIG.Window.Height)
        self.setWindowIcon(QtGui.QPixmap("./Resource/icon/ffm_main.png"))

        # window flags: No borders, always top, hide taskbar ICONS.
        _attribute = QtCore.Qt.FramelessWindowHint | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.Tool
        # self.stayOnTop()
        # self.showInTaskBar()
        if CONFIG.Window.AlwaysOnTop:
            _attribute |= QtCore.Qt.WindowStaysOnTopHint
        if CONFIG.Window.ShowInTaskBar:
            _attribute &= ~QtCore.Qt.Tool

        self.setWindowFlags(_attribute)

        # The background transparent.
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        # To track the mouse
        self.setMouseTracking(True)

        # Set tray menu.
        self.setTrayMenu()

        # Set tray attribute.
        self.trayIcon = QtGui.QSystemTrayIcon()
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QtGui.QIcon("./Resource/icon/ffm_main.png"))
        self.trayIcon.setToolTip(CONFIG.Main.Name)
        self.trayIcon.activated.connect(self.onTrayIconActivated)
        self.trayIcon.show()

        # Set animation.
        self.ani = QtCore.QPropertyAnimation(self, b"geometry")
        self.ani.setDuration(self._AnimationTime)
        self.ani.finished.connect(self._setAniFinish)

        self.initUI()

    def initUI(self):
        titleWidget = self.findChild(QtGui.QWidget, "titleWidget")
        self.titleBar = TitleWidget(titleWidget)
        # self.titleBar.setAutoFillBackground(True)
        self._mainLayout.addWidget(self.titleBar)

        self.titleBar.windowMinimumed.connect(self.showMinimized)
        # self.titleBar.windowMaximumed.connect(self.showMaximized)
        # self.titleBar.windowNormaled.connect(self.showNormal)
        self.titleBar.windowClosed.connect(self.close)
        self.titleBar.windowMoved.connect(self.move)
        self.titleBar.windowReleased.connect(self.hideWindow)

    # def stayOnTop(self):
    #     _attribute = self.windowFlags()
    #     if CONFIG.Window.AlwaysOnTop:
    #         _attribute |= QtCore.Qt.WindowStaysOnTopHint
    #     else:
    #         _attribute &= ~QtCore.Qt.WindowStaysOnTopHint
    #
    #     self.setWindowFlags(_attribute)
    #
    # def showInTaskBar(self):
    #     _attribute = self.windowFlags()
    #     if CONFIG.Window.ShowInTaskBar:
    #         _attribute &= ~QtCore.Qt.Tool
    #     else:
    #         _attribute |= QtCore.Qt.Tool
    #
    #     self.setWindowFlags(_attribute)

    def setTrayMenu(self):
        self.trayIconMenu = QtGui.QMenu()
        self.testAction = self.trayIconMenu.addAction("test")
        self.testAction.triggered.connect(self.testHandle)

    def testHandle(self):
        print "testHandle"

    def onTrayIconActivated(self, reason):
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
            self.raise_()
            self.activateWindow()
            self.showNormal()

    def _setAniFinish(self):
        self._ani_finish = True

    def setWidget(self, widget):
        """
        Add custom widget.
        :param widget: custom widget, type: QWidget
        """
        if hasattr(self, '_widget'):
            return
        self._widget = widget
        # Set the default background color, otherwise it will
        # be transparent due to the influence of the parent window.
        self._widget.setAutoFillBackground(True)
        palette = self._widget.palette()
        palette.setColor(palette.Window, QtGui.QColor(240, 240, 240))
        self._widget.setPalette(palette)
        self._widget.installEventFilter(self)
        self.layout().addWidget(self._widget)

    def move(self, pos):
        if self.windowState() == QtCore.Qt.WindowMaximized\
                or self.windowState() == QtCore.Qt.WindowFullScreen:
            # Conditions that do not permit movement.
            return
        _x = pos.x()
        _y = pos.y()
        # Go to the edge of the screen and no longer move outward.
        if pos.y() < 0:
            _y = 0
        if pos.y() > self._win_height - 100:
            # If not sinking at all, use "self._win_height - self.height()"
            _y = self._win_height - 100
        if pos.x() < 0:
            _x = 0
        if pos.x() > self._win_width - self.width():
            _x = self._win_width - self.width()
        _pos = QtCore.QPoint(_x, _y)
        super(FramelessWidget, self).move(_pos)

    def hideWindow(self):
        if self.y() < 0:
            self.windowHideAni()

    def windowShowAni(self):
        if CONFIG.Window.CloseEdgeHide:
            self.ani.stop()
            self._ani_finish = False
            self.ani.setStartValue(QtCore.QRect(self.x(), 6 - self.height(), self.width(), self.height()))
            self.ani.setEndValue(QtCore.QRect(self.x(), 0, self.width(), self.height()))
            self.ani.start()

    def windowHideAni(self):
        if CONFIG.Window.CloseEdgeHide:
            self.ani.stop()
            self._ani_finish = False
            self.ani.setStartValue(QtCore.QRect(self.x(), 0, self.width(), self.height()))
            self.ani.setEndValue(QtCore.QRect(self.x(), 6 - self.height(), self.width(), self.height()))
            self.ani.start()

    # def showMaximized(self):
    #     super(JWidget, self).showMaximized()
    #     self.layout().setContentsMargins(0, 0, 0, 0)
    #
    def showNormal(self):
        """
        Restore to retain the upper and lower left and right
        borders, or no border can not be adjusted
        """
        super(FramelessWidget, self).showNormal()
        self.layout().setContentsMargins(
            self.Margins, self.Margins, self.Margins, self.Margins)
        y = self.y()
        y -= 2
        if y < 0:
            self.windowHideAni()

    def paintEvent(self, event):
        """
        Since it is a fully transparent background window,
        the redraw event draws an invisible border with a
        transparency of 1, used to resize the window.
        """
        super(FramelessWidget, self).paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 1), self.Margins * 2))
        painter.drawRect(self.rect())

    def eventFilter(self, obj, event):
        """
        Event filter that restores to standard mouse style
        after mouse entry into other controls.
        """
        if isinstance(event, QtGui.QMouseEvent):
            self.setCursor(QtCore.Qt.ArrowCursor)
        return super(FramelessWidget, self).eventFilter(obj, event)

    def enterEvent(self, event):
        """Used to pop up a display window"""
        if self._ani_finish == False:
            # Invalid if animation is in progress.
            return

        super(FramelessWidget, self).enterEvent(event)
        y = self.y()
        if y < 0:
            self.windowShowAni()

    def leaveEvent(self, event):
        """
        If the original window is already hidden and temporarily
        displayed, it needs to be hidden again after leaving.
        """
        if self._ani_finish == False:
            # Invalid if animation is in progress
            return

        super(FramelessWidget, self).leaveEvent(event)
        y = self.y()
        y -= 2
        if y < 0:
            self.windowHideAni()

    def mousePressEvent(self, event):
        super(FramelessWidget, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self._mpos = event.pos()
            self._pressed = True

    def mouseReleaseEvent(self, event):
        super(FramelessWidget, self).mouseReleaseEvent(event)
        self.setCursor(QtCore.Qt.ArrowCursor)
        self._pressed = False
        self.Direction = None

    def mouseMoveEvent(self, event):
        super(FramelessWidget, self).mouseMoveEvent(event)
        pos = event.pos()
        xPos, yPos = pos.x(), pos.y()
        # Move.
        wm, hm = self.width() - self.Margins, self.height() - self.Margins
        if self.isMaximized() or self.isFullScreen():
            self.Direction = None
            self.setCursor(QtCore.Qt.ArrowCursor)
            return
        if event.buttons() == QtCore.Qt.LeftButton and self._pressed:
            self._resizeWidget(pos)
            return
        # Mouse on different direction.
        if xPos <= self.Margins and yPos <= self.Margins:
            # LeftTop
            self.Direction = JzChat.LeftTop
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
            # RightBottom
            self.Direction = JzChat.RightBottom
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif wm <= xPos and yPos <= self.Margins:
            # RightTop
            self.Direction = JzChat.RightTop
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        elif xPos <= self.Margins and hm <= yPos:
            # LeftBottom
            self.Direction = JzChat.LeftBottom
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        elif 0 <= xPos <= self.Margins and self.Margins <= yPos <= hm:
            # Left
            self.Direction = JzChat.Left
            self.setCursor(QtCore.Qt.SizeHorCursor)
        elif wm <= xPos <= self.width() and self.Margins <= yPos <= hm:
            # Right
            self.Direction = JzChat.Right
            self.setCursor(QtCore.Qt.SizeHorCursor)
        elif self.Margins <= xPos <= wm and 0 <= yPos <= self.Margins:
            # Top
            self.Direction = JzChat.Top
            self.setCursor(QtCore.Qt.SizeVerCursor)
        elif self.Margins <= xPos <= wm and hm <= yPos <= self.height():
            # Bottom
            self.Direction = JzChat.Bottom
            self.setCursor(QtCore.Qt.SizeVerCursor)

    def _resizeWidget(self, pos):
        if self.Direction == None:
            return
        mpos = pos - self._mpos
        xPos, yPos = mpos.x(), mpos.y()
        geometry = self.geometry()
        # How to adjust by "self.Direction" judgment.
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()
        if self.Direction == JzChat.LeftTop:
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
        elif self.Direction == JzChat.RightBottom:
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos = pos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos = pos
        elif self.Direction == JzChat.RightTop:
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos.setX(pos.x())
        elif self.Direction == JzChat.LeftBottom:
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos.setY(pos.y())
        elif self.Direction == JzChat.Left:
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            else:
                return
        elif self.Direction == JzChat.Right:
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos = pos
            else:
                return
        elif self.Direction == JzChat.Top:
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            else:
                return
        elif self.Direction == JzChat.Bottom:
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos = pos
            else:
                return
        self.setGeometry(x, y, w, h)


class MainPanel(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainPanel, self).__init__(*args, **kwargs)
        self._layout = QtGui.QVBoxLayout(self, spacing=0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._init_show_flag = True
        self.TabAnimationTime = CONFIG.Window.TabAnimationTime

        self.setObjectName("MainPanel")

        css_name = "./Resource/css/main.css"
        with open(css_name, 'r') as css_file:
            style_sheet = css_file.read()
        self.setStyleSheet(style_sheet)

        self.initUI()
        self.selfAvatar.setPixmap(circleAvatar(self.selfAvatar.width(), "./Resource/image/avatar.png"))
        self.addUser()
        self.addGroup()
        self.setBackground()

    def initUI(self):
        win = UILoader("./Resource/ui/main.ui")
        win.setAutoFillBackground(True)
        self._layout.addWidget(win)

        self.selfInfoWidget = self.findChild(QtGui.QWidget, "selfInfo")

        self.selfAvatar = self.findChild(QtGui.QWidget, "selfAvatar")
        self.selfUsername = self.findChild(QtGui.QWidget, "selfUsername")
        self.selfUserInfo = self.findChild(QtGui.QWidget, "selfUserInfo")
        self.selfState = self.findChild(QtGui.QWidget, "selfState")
        self.userScrollArea = self.findChild(QtGui.QScrollArea, "userScrollArea")
        self.userScrollArea.setViewportMargins(0, 0, 0, 0)
        self.groupScrollArea = self.findChild(QtGui.QScrollArea, "groupScrollArea")
        self.groupScrollArea.setViewportMargins(0, 0, 0, 0)
        self.groupScrollArea.hide()  # Init is hide.

        self.personListBtn = self.findChild(QtGui.QPushButton, "personListBtn")
        self.personListBtn.clicked.connect(self.showPersonList)

        self.groupListBtn = self.findChild(QtGui.QPushButton, "groupListBtn")
        self.groupListBtn.clicked.connect(self.showGroupList)

        self.layout().addWidget(FooterWidget())

    def setBackground(self):
        _palette = QtGui.QPalette()
        _pixmap = QtGui.QPixmap("./Resource/image/background_info_2.png").scaled(
            self.selfInfoWidget.width(), self.selfInfoWidget.height(),
            QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        _palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(_pixmap))
        self.selfInfoWidget.setPalette(_palette)

    def showPersonList(self):
        if self.userScrollArea.isVisible():
            return

        if CONFIG.Window.TabAnimationValid:
            _width = self.width() - 4  # border 2, left + right = 4
            _height = self.userScrollArea.height()

            g_x = self.groupScrollArea.x()
            g_y = self.groupScrollArea.y()
            p_x = self.userScrollArea.x()
            p_y = self.userScrollArea.y()

            # hide group list.
            self.spgAni = QtCore.QPropertyAnimation(self.groupScrollArea, b"geometry")
            self.spgAni.setDuration(self.TabAnimationTime)
            self.spgAni.setStartValue(QtCore.QRect(g_x, g_y, _width, _height))
            self.spgAni.setEndValue(QtCore.QRect(g_x + _width, g_y, _width, _height))
            self.spgAni.start()
            self.spgAni.finished.connect(lambda: self.groupScrollArea.hide())

            # show person list.
            self.userScrollArea.show()
            self.sppAni = QtCore.QPropertyAnimation(self.userScrollArea, b"geometry")
            self.sppAni.setDuration(self.TabAnimationTime)
            self.sppAni.setStartValue(QtCore.QRect(p_x, p_y, _width, _height))
            self.sppAni.setEndValue(QtCore.QRect(p_x + _width, p_y, _width, _height))
            self.sppAni.start()
        else:
            self.groupScrollArea.hide()
            self.userScrollArea.show()

    def showGroupList(self):
        if self.groupScrollArea.isVisible():
            return

        if CONFIG.Window.TabAnimationValid:
            _width = self.width() - 4  # border 2, left + right = 4
            _height = self.userScrollArea.height()

            g_x = self.groupScrollArea.x()
            g_y = self.groupScrollArea.y()
            p_x = self.userScrollArea.x()
            p_y = self.userScrollArea.y()

            if self._init_show_flag:  # There is no height for initializing the Group widget.
                self._init_show_flag = False
                g_y = p_y
                g_x += _width

            # hide person list.
            self.sppAni = QtCore.QPropertyAnimation(self.userScrollArea, b"geometry")
            self.sppAni.setDuration(self.TabAnimationTime)
            self.sppAni.setStartValue(QtCore.QRect(p_x, p_y, _width, _height))
            self.sppAni.setEndValue(QtCore.QRect(p_x - _width, p_y, _width, _height))
            self.sppAni.start()
            self.sppAni.finished.connect(lambda: self.userScrollArea.hide())

            # show group list.
            self.groupScrollArea.show()
            self.spgAni = QtCore.QPropertyAnimation(self.groupScrollArea, b"geometry")
            self.spgAni.setDuration(self.TabAnimationTime)
            self.spgAni.setStartValue(QtCore.QRect(g_x, g_y, _width, _height))
            self.spgAni.setEndValue(QtCore.QRect(g_x - _width, g_y, _width, _height))
            self.spgAni.start()
        else:
            self.userScrollArea.hide()
            self.groupScrollArea.show()

    def addUser(self):
        # items = [_ for _ in range(15)]
        _userWrapWidget = QtGui.QWidget(self)
        # Lateral stretch, longitudinal fixation.
        _userWrapWidget.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        listBox = QtGui.QVBoxLayout(spacing=0)
        listBox.setContentsMargins(0, 0, 0, 0)
        listBox.setAlignment(QtCore.Qt.AlignTop)
        _userWrapWidget.setLayout(listBox)

        # for item in items:
            # userItem = UserItem(item)
            # listBox.addWidget(userItem)

        listBox.addWidget(CategoryItem("Group1"))
        listBox.addWidget(CategoryItem("Group2"))
        listBox.addWidget(CategoryItem("Group3"))

        self.userScrollArea.setWidget(_userWrapWidget)

    def addGroup(self):
        _groupWrapWidget = QtGui.QWidget(self)
        # Lateral stretch, longitudinal fixation.
        _groupWrapWidget.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        listBox = QtGui.QVBoxLayout(spacing=0)
        listBox.setContentsMargins(0, 0, 0, 0)
        listBox.setAlignment(QtCore.Qt.AlignTop)
        _groupWrapWidget.setLayout(listBox)

        for _ in range(5):
            groupItem = GroupItem("")
            listBox.addWidget(groupItem)

        self.groupScrollArea.setWidget(_groupWrapWidget)


    def enterEvent(self, event):
        """Set mouse style."""
        self.setCursor(QtCore.Qt.ArrowCursor)
        super(MainPanel, self).enterEvent(event)


class FooterWidget(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(FooterWidget, self).__init__(*args, **kwargs)
        self._layout = QtGui.QVBoxLayout(self, spacing=0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.setObjectName("FooterWidget")

        css_name = "./Resource/css/footer.css"
        with open(css_name, 'r') as css_file:
            style_sheet = css_file.read()
        self.setStyleSheet(style_sheet)

        self.initUI()

    def initUI(self):
        win = UILoader("./Resource/ui/footer.ui")
        win.setAutoFillBackground(True)
        self._layout.addWidget(win)

        self.menuBtn = self.findChild(QtGui.QPushButton, "menuBtn")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./Resource/icon/settings1.png"))
        self.menuBtn.setIcon(icon)
        size = QtCore.QSize(self.menuBtn.width() - 3, self.menuBtn.height() - 3)
        self.menuBtn.setIconSize(size)
        self.menuBtn.clicked.connect(self.menuHandle)

    def menuHandle(self):
        sd = SettingDialog(self)
        sd.exec_()



def run():
    app = QtGui.QApplication(sys.argv)

    # Load font file.
    fontId = QtGui.QFontDatabase.addApplicationFont("./Resource/font/msyh.ttc")
    font = QtGui.QFontDatabase.applicationFontFamilies(fontId)[0]
    app.setFont(QtGui.QFont(font))

    app.setQuitOnLastWindowClosed(False)  # close window do not exit.
    t = FramelessWidget()
    t.setWidget(MainPanel())
    widget.WIDGET = t
    t.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run()
