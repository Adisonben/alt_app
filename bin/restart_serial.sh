#!/bin/bash
cd /home/pi/alcohol_tester_iddrives/
rm -rf ./cache/arduino/*.json
for pid in $(/usr/bin/pgrep -f bin/RunTime_SerialRead.py)
do
	#echo "KILL PID:" $pid
	sudo /bin/kill -9 $pid
done

#/usr/bin/screen -dmS zxc /usr/bin/python bin/RunTime_SerialRead.py 
#/usr/bin/screen -wipe

/usr/bin/nohup /usr/bin/python bin/RunTime_SerialRead.py > cache/runtime_serial.log 2>&1 &
