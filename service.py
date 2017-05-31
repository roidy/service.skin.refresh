# -*- coding: utf-8 -*-

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import kodiutils
import kodilogging

import logging
import time
import xbmc
import xbmcaddon


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))

class Watcher:
    
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, ADDON.getSetting('skinpath'), recursive=True)
        self.observer.start()

        try:
            monitor = xbmc.Monitor()
            
            while not monitor.abortRequested():
                # Sleep/wait for abort for 3 seconds
                if monitor.waitForAbort(3):
                    # Abort was requested while waiting. We should exit
                    self.observer.stop()
                    exit()

        except Exception as e:
            self.observer.stop()
            logger.info("Error: %s" % e)

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            logger.info("File created: %s" % event.src_path)

        elif event.event_type == 'modified':
            logger.info("File modified: %s" % event.src_path)
            # A file has been modified, reload the skin
            xbmc.executebuiltin('XBMC.ReloadSkin()')

def run():
    
    # If watched_directory isn't set then open settings
    if ADDON.getSetting('skinpath') == "":
        addon.openSettings()

    # If user still hasn't set a watched directory then exit
    if ADDON.getSetting('skinpath') == "":
        logger.error("No skin path set, quitting service.")
        exit()
        
    logger.info("Watching directory: %s" % ADDON.getSetting('skinpath'))
    
    # Create and start file system watcher
    w = Watcher()
    w.run()

    
            
        
