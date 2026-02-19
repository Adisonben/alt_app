#!/bin/bash

sleep 1

xset s off
xset -dpms
xset -display :0.0 dpms force on
xset s noblank
sed -i 's/"exited_cleanly": false/"exited_cleanly": true/' ~/.config/chromium/Default/Preferences


/usr/bin/chromium-browser \
	--disable-gpu \
	--disable-translate \
	--force-device-scale-factor \
	--noerrdialogs \
	--disable-session-crashed-bubble \
	--incognito \
	--disable-infobars \
	--kiosk \
	--disable-pinch \
	--auto \
	--overscroll-history-navigation=0 \
	http://127.0.0.1/app

#	https://www.google.co.th
#	http://192.168.22.199/bus2/index.html
#	http://192.168.137.1/bus2/index.html
