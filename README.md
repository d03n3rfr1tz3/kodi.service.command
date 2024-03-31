# service.command
A simple service for Kodi, with which you can activate commands on idle/wake or other events.

## How To
Install the service via ZIP installation. The service will create `.sh` files in its data directory, when the corresponding events happen. You can then edit these `.sh` files to run your desired commands. Obviously this is centered around a linux host.

## Example
Imagine you have the BOINC addon in your Kodi calculating stuff for science. BOINC allows some configuration to only use a certain amount of CPU time, when the CPU is not occupied over a treshold value. But for that to happen, you have to start something that uses the CPU and then wait that BOINC recognizes that. On Kodi that might lead to a laggy menu or weird behavior at the start of a movie or something like that. To make sure BOINC is paused, when you actually want to use your Kodi, you could pause/unpause it on activation/deactivation of the screensaver, like I did. That way BOINC would only run for a while on startup and when the screensaver is active.

`onScreensaverActivated.sh` --> add `docker unpause boinc` \
`onScreensaverDeactivated.sh` --> add `docker pause boinc`
