#!/usr/bin/sh
import sys,json,time,os

def response(name="mag",session="0"):
	status = "OK"
	read = {}
	while True:
		time.sleep(0.05)
		if os.path.isfile('./cache/arduino/'+session+'.'+name+'.json'):
			break
	file = open('./cache/arduino/'+session+'.'+name+'.json', "r")
	try:
		read = json.loads(file.read())
		read['status'] = read['status'].upper()
	except:
		status = "FAIL"
	if status == 'FAIL':
		read['status'] = "FAIL"
		read['session'] = "0"
	os.system('rm -rf ./cache/arduino/'+session+'.'+name+'.json')
	return json.dumps(read, indent=2, sort_keys=True)

print response(sys.argv[1],sys.argv[2])
