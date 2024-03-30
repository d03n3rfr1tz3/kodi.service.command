import os
import subprocess
import sys
import xbmc
import xbmcaddon
import xbmcvfs

addon = xbmcaddon.Addon('service.command')
addon_data = addon.getAddonInfo('profile')

class EventCommands():

    class EventMonitor(xbmc.Monitor):
    
        def __init__(self, onEvent):
            self.onEvent = onEvent

        def onCleanStarted(self):
            self.onEvent(sys._getframe().f_code.co_name)

        def onCleanFinished(self):
            self.onEvent(sys._getframe().f_code.co_name)

        def onDPMSActivated(self):
            self.onEvent(sys._getframe().f_code.co_name)

        def onDMPSDeactivated(self):
            self.onEvent(sys._getframe().f_code.co_name)

        def onScanStarted(self):
            self.onEvent(sys._getframe().f_code.co_name)

        def onScanFinished(self):
            self.onEvent(sys._getframe().f_code.co_name)

        def onScreensaverActivated(self):
            self.onEvent(sys._getframe().f_code.co_name)
        
        def onScreensaverDeactivated(self):
            self.onEvent(sys._getframe().f_code.co_name)

    def onInit(self):
        folder_path = xbmcvfs.translatePath(addon_data)
        self.preparePath(folder_path)

        monitor = self.EventMonitor(self.onEvent)
        while not monitor.abortRequested():
            if monitor.waitForAbort(10):
                break

    def onEvent(self, eventName):
        folder_path = xbmcvfs.translatePath(addon_data)
        self.preparePath(folder_path)

        file_path = folder_path + eventName + '.sh'
        self.prepareFile(file_path)

        self.executeCommand(file_path)

    def preparePath(self, folder_path):
        if not xbmcvfs.exists(folder_path):
            xbmcvfs.mkdir(folder_path)

    def prepareFile(self, file_path):
        if not os.path.exists(file_path):
            file_descriptor = os.open(
                path=file_path,
                flags=(os.O_WRONLY | os.O_CREAT | os.O_TRUNC),
                mode=0o777
            )
            with open(file_descriptor, 'w') as fh:
                fh.write('#!/bin/sh')

    def executeCommand(self, command_path):
        subprocess.run(['/bin/sh', command_path])

if __name__ == '__main__':
    eventCommands = EventCommands()
    eventCommands.onInit()
    del eventCommands