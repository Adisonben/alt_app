#!/bin/bash
#export DISPLAY=:0

cd /home/pi/alcohol_tester_iddrives/bin
nohup killall screen > /dev/null 2>&1&

#echo "Delay for 5sec [FIX BUG STARTUP]"
sleep 2

#echo "## RUN API ##"
/usr/bin/sudo -u pi /usr/bin/screen -dmS api-log ./auto_run_api.sh
#sudo -u pi screen -dmS api-log python api.py
