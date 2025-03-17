import os
import subprocess
import stat
import sys
import xbmc
import xbmcaddon
import xbmcvfs

addon = xbmcaddon.Addon('service.command')
addon_data = addon.getAddonInfo('profile')

class EventCommands():
    aborted = False
    idled = xbmc.getGlobalIdleTime()

    class EventMonitor(xbmc.Monitor):
    
        def __init__(self, onEvent):
            self.onEvent = onEvent

        def onScanStarted(self, library):
            self.onEvent(sys._getframe().f_code.co_name)

        def onScanFinished(self, library):
            self.onEvent(sys._getframe().f_code.co_name)

        def onCleanStarted(self, library):
            self.onEvent(sys._getframe().f_code.co_name)

        def onCleanFinished(self, library):
            self.onEvent(sys._getframe().f_code.co_name)

        def onDPMSActivated(self):
            self.onEvent(sys._getframe().f_code.co_name)

        def onDMPSDeactivated(self):
            self.onEvent(sys._getframe().f_code.co_name)

        def onScreensaverActivated(self):
            self.onEvent(sys._getframe().f_code.co_name)

        def onScreensaverDeactivated(self):
            self.onEvent(sys._getframe().f_code.co_name)

    class EventPlayer(xbmc.Player):
    
        def __init__(self, onEvent):
            self.onEvent = onEvent

        def onPlayBackStarted(self):
            self.onEvent(sys._getframe().f_code.co_name)

        def onPlayBackStopped(self):
            self.onEvent(sys._getframe().f_code.co_name)

        def onPlayBackEnded(self):
            self.onEvent(sys._getframe().f_code.co_name)

        def onPlayBackPaused(self):
            self.onEvent(sys._getframe().f_code.co_name)

        def onPlayBackResumed(self):
            self.onEvent(sys._getframe().f_code.co_name)

    def onInit(self):
        folder_path = xbmcvfs.translatePath(addon_data)
        self.preparePath(folder_path)

        monitor = self.EventMonitor(self.onEvent)
        player = self.EventPlayer(self.onEvent)
        while not monitor.abortRequested():

            if monitor.waitForAbort(1):
                self.aborted = True
                break

            oldIdled = self.idled
            newIdled = xbmc.getGlobalIdleTime()
            self.idled = newIdled

            if newIdled >= 10 and oldIdled < 10:
                self.onEvent("onIdleStart")
            if oldIdled >= 10 and newIdled < oldIdled:
                self.onEvent("onIdleEnd")

    def onEvent(self, eventName):
        if self.aborted: return

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
            xbmc.log("Script '{0}' will be prepared now.".format(file_path))
            with open(file_path, 'w') as fh:
                fh.write('#!/bin/sh')

            st = os.stat(file_path)
            os.chmod(file_path, st.st_mode | stat.S_IEXEC)

    def executeCommand(self, command_path):
        xbmc.log("Script '{0}' will be executed now.".format(command_path))
        subprocess.run(['/bin/sh', command_path])

if __name__ == '__main__':
    eventCommands = EventCommands()
    eventCommands.onInit()
    del eventCommands
