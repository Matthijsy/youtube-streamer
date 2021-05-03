# Automatic YouTube streamer
Small project to automate the streaming to youtube. It uses the OBS websocket to automatically switch scenes and start/stop the service. 


## Installation
1. Get a fresh installation of Debian
1. Install [OBS Studio](https://obsproject.com/wiki/install-instructions#linux)
1. Install drivers for the video capture card ([Blackmagic](https://www.blackmagicdesign.com/support/family/capture-and-playback) in my case)
1. Install [obs-websockets](https://obsproject.com/forum/resources/obs-websocket-remote-control-obs-studio-from-websockets.466/)
1. Install [https://wiki.debian.org/acpid](https://wiki.debian.org/acpid) (used for interacting with the power button)
1. Install [Beep](https://packages.debian.org/unstable/beep) (used for alarm when no connection)
1. Copy the files of `localfiles/autostart` to `~/.config/autostart` on the machine.
1. Add the lines in `localfiles/sudoers.txt` to the sudoers file using `sudo visudo`
1. Edit `/etc/systemd/logind.conf` and add the line `HandlePowerKey=ignore`

## Quick overview
This project automatically starts OBS on startup, then the main script is called. This will try to interact with OBS and start the stream. YouTube should be configured to automatically go live when it receives signal. 

In our case we have configured 2 scenes in OBS, one for pre-service and one live. The pre-service scene only broadcasts static audio and a image. Then when the button is clicked OBS will switch to the live video input and stream the real service. After 2 consecutive pushes on the power button again the system stops the stream and shutsdown.


## Remote control
It is possible to control the system via teamviewer. In order to do that install `xserver-xorg-video-dummy` and place the `localfiles/xorg.conf` in `/etc/X11/xorg.conf`. Now install teamviewer and you can access it remotely. Disadvantage of this is that the local output won't work after this.