import serial
import sys

try:
	# /dev/ttyACM0 # /dev/ttyUSB0
	ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=0.1041666666667)
except Exception as e: 
	print e
except:
	print "OPEN_PORT_ERROR"
	
try:
	if len(sys.argv) <= 1:
		sys.exit("NO_ARGV")
	else:
		ser.write(sys.argv[1])
		print "SEND_OK"
except Exception as e: 
	print e
