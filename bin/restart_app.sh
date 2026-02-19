#!/bin/bash

cd /home/pi/alcohol_tester_iddrives/bin

echo "## STOP APP ##"
sh stop_app.sh
sh stop_api.sh
echo "## START APP ##"
sleep 4
sh run_api.sh
sh run_screen_app.sh

echo "## SHELL SUCCESS ##"
