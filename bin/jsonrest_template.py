#!/usr/bin/sh
import sys,json,time,os,subprocess

def response(name="mag",session="0"):
	if name != 'mag':
		time.sleep(3)
	subprocess.Popen('rm -rf bin/arduino_json_template/*.txt', shell=True, stdout=subprocess.PIPE).stdout.read().strip()
	while True:
		time.sleep(0.1)
		if os.path.isfile('bin/arduino_json_template/'+session+'.txt'):
			break
	file = open("bin/arduino_json_template/"+name+".json", "r") 
	read = json.loads(file.read())
	read['session'] = session
	read['status'] = read['status'].upper()
	subprocess.Popen('rm -rf bin/arduino_json_template/*.txt', shell=True, stdout=subprocess.PIPE).stdout.read().strip()
	return json.dumps(read)
print response(sys.argv[1],sys.argv[2])
