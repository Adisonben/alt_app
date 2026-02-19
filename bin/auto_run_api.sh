#!/bin/bash

cd /home/pi/alcohol_tester_iddrives/
while :
do
	/usr/bin/python api.py
	/bin/sleep 2
done
