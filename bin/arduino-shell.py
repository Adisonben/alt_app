import time
import serial
import json
import sys
import threading

ser = serial.Serial(
			port='/dev/ttyUSB0',
			baudrate = 9600,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			timeout=0.104
)

#ser.write('mag&4984165;')
def BackgroundRead():
	global ser
	global readTh
	global myData
	readTh = False
	while True:
		try:
			if(ser.inWaiting()>0):
				myData = ser.readline()
			else:
				readTh = True
		except:
			pass

def arduino(cmd):
	global ser
	global readTh
	global myData
	if readTh:
		name = raw_input("enter>")
		ser.write(cmd)
		while True:
			timeest = time.time()
			while True:
				try:
					time.sleep(0.00001)
					buf = myData
				except:
					pass
				else:
					print myData
					del myData
					break
			print (time.time()-timeest)
			name = raw_input("enter>")
			ser.write('test&2000;')
				
	else:
		print "Read Thread Not Start"
		sys.exit()


if __name__ == "__main__":
	thread = threading.Thread(target=BackgroundRead,)
	thread.daemon = False
	thread.start()
	
	print "Delay for serial read thread"
	time.sleep(1)

	arduino('0000')
