# -*- coding: utf-8 -*-

import kodilogging
import service

import logging
import xbmcaddon

ADDON = xbmcaddon.Addon()
kodilogging.config()

service.run()


