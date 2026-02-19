#!/bin/bash

for i in {1..58}
do

	API_PID=`pidof /usr/bin/python api.py`
	CNT_API=`echo $API_PID | wc -w`

	if [ "$CNT_API" -lt "2" ] ; then
		/home/pi/alcohol_tester_iddrives/bin/stop_api.sh	
		sleep 1
		/home/pi/alcohol_tester_iddrives/bin/run_api.sh
		sudo -u pi echo $(date) >> /home/pi/alcohol_tester_iddrives/cache/api_stop.log
	else
		echo "API RUN"
	fi
	sleep 1

done
