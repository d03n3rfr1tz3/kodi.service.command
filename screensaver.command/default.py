import os
import subprocess
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs

addon = xbmcaddon.Addon('screensaver.command')
addon_name = addon.getAddonInfo('name')
addon_path = addon.getAddonInfo('path')
addon_data = addon.getAddonInfo('profile')

class Screensaver(xbmcgui.WindowXMLDialog):

    class ExitMonitor(xbmc.Monitor):

        def __init__(self, exit_callback):
            self.exit_callback = exit_callback

        def onScreensaverDeactivated(self):
            self.exit_callback()

    def onInit(self):
        if not xbmcvfs.exists(xbmcvfs.translatePath(addon_data)):
            xbmcvfs.mkdir(xbmcvfs.translatePath(addon_data))

        file_path = xbmcvfs.translatePath(addon_data) + 'on_idle.sh'
        if not os.path.exists(file_path):
            file_descriptor = os.open(
                path=file_path,
                flags=(os.O_WRONLY | os.O_CREAT | os.O_TRUNC),
                mode=0o777
            )
            with open(file_descriptor, 'w') as fh:
                fh.write('#!/bin/bash')

        subprocess.call(file_path, shell=True)
        self.monitor = self.ExitMonitor(self.exit)

    def exit(self):
        if not xbmcvfs.exists(xbmcvfs.translatePath(addon_data)):
            xbmcvfs.mkdir(xbmcvfs.translatePath(addon_data))

        file_path = xbmcvfs.translatePath(addon_data) + 'on_wake.sh'
        if not os.path.exists(file_path):
            file_descriptor = os.open(
                path=file_path,
                flags=(os.O_WRONLY | os.O_CREAT | os.O_TRUNC),
                mode=0o777
            )
            with open(file_descriptor, 'w') as fh:
                fh.write('#!/bin/bash')

        subprocess.call(file_path, shell=True)
        self.close()


if __name__ == '__main__':
    screensaver = Screensaver(
            'script-main.xml',
            addon_path,
            'default',
        )
    screensaver.doModal()
    del screensaver
    sys.modules.clear()
