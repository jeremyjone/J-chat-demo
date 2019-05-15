# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = "jeremyjone"
__datetime__ = "2019/5/7 14:00"
__all__ = ["JConfig"]

import configparser, os


class JConfig(object):
    def __init__(self, configFile):
        """
        :param configFile: config file path
        """

        self.__config_file = configFile

        self.__config = configparser.ConfigParser()
        self.__config.read(self.__config_file, encoding='UTF-8')

    def getConfig(self, section, key):
        try:
            return self.__config.get(section, key)
        except:
            raise

    def setConfig(self, section, key, value):
        try:
            self.__config.add_section(section)
        except:
            pass

        self.__config.set(section, key, value)
        self.__config.write(open(self.__config_file, 'w'))

    def delConfig(self, section, key=None):
        try:
            if key is None:
                self.__config.remove_section(section)
            else:
                self.__config.remove_option(section, key)
        except:
            return

        self.__config.write(open(self.__config_file, 'w'))

    def delKey(self, section, key):
        try:
            self.__config.remove_option(section, key)
        except:
            return

        self.__config.write(open(self.__config_file, 'w'))

    def getAllSections(self):
        return self.__config.sections()

    def getAllKeys(self, section):
        return self.__config.options(section)

    @property
    def config(self):
        return self.__config