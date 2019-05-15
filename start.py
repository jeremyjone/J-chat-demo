# !/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Main start file, show app's version.
"""
__author__ = "jeremyjone"
__datetime__ = "2019/4/30 18:02"
__all__ = ["__version__"]
__version__ = "0.1Beta"


from widget import mainWidget


if __name__ == '__main__':
    mainWidget.run()  # Start apps

