#!/usr/bin/python

import serial
import sys,os,json,time,subprocess
#from serial.tools import list_ports

port='/dev/ttyACM0' # /dev/ttyACM0 # /dev/ttyUSB0
state=False
# https://pyserial.readthedocs.io/en/latest/tools.html

while state == False:
	print

	if os.system('rm -rf ./cache/arduino/*.json') == True:
		print "Clear cache: OK"
	else:
		print "Clear cache: FAIL"

	try:
		ser = serial.Serial(port, baudrate=9600, timeout=0.1041666666667)
		print "Port: "+port
		print "Port Open: "+str(ser.isOpen())
		print
		state = ser.isOpen()
	except Exception as e: 
		print e
	except:
		print "OPEN_PORT_ERROR"
	time.sleep(1)

print subprocess.Popen('python ./bin/SendSerial.py \'dmag&0;\'', shell=True, stdout=subprocess.PIPE).stdout.read()

while True:
	line = ser.readline()
	if line:
		os.system('echo \''+line+'\' >> ./cache/arduino/line.log')
		try:
			jsload = json.loads(line)
		except Exception as e:
			print e
			jsload = json.loads('{"session":"0","status":"FAIL","cmd":"mag","results":""}')

		if jsload["status"] != 'FINGERSCAN':
			data = json.dumps(jsload, indent=2, sort_keys=True)
			print data
			os.system('echo \''+data+'\' > ./cache/arduino/'+jsload['session']+'.'+jsload['cmd']+'.json')
			os.system('echo \''+data+'\' >> ./cache/arduino/data.log')
		else:
			data = json.dumps(jsload, indent=2, sort_keys=True)
			print data
			os.system('echo \''+data+'\' >> ./cache/arduino/data.log')
'''
while True:
		if(ser.inWaiting()>0):
			myData = ser.readline()
			print myData
			#break
'''
#ser.close()
#sys.exit()

'''
def scan():
	available = []
	for i in range(256):
		try:
			s = serial.Serial(i)
			available.append( (i, s.portstr))
			s.close() # explicit close 'cause of delayed GC in java
		except serial.SerialException:
			pass
	return available

if __name__=='__main__':
	print ("Found ports:")
	for n,s in scan():
		print ("(%d) %s" % (n,s))
		selection = input("Enter port number:")
'''

'''
import serial
import sys,json

while True:
	try:
		ser = serial.Serial(
			port='/dev/ttyACM0',   # /dev/ttyACM0 # /dev/ttyUSB0
			baudrate = 115200,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			timeout=0.1
		)

		myData = ""
		while True:
			if(ser.inWaiting()>0):
				myData = ser.readline()
				print myData
				#ses = json.loads(myData)
				#file = open("./cache/arduino_cache/"+ses['session']+".json","w")
				#file.write(myData)
				#file.close()
				#break
	except KeyboardInterrupt:
		sys.exit()
	except Exception as e: 
		print e
	except:
		print "READ_ERROR"
#ser.close()
#sys.exit()

'''
