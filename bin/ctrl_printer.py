import signal,subprocess,os,requests,sys,json,time

output = ""

def TimeOut(atimeout, *args):
    def decorate(f):
        def handler(signum, frame):
            raise TimedOutExc()
        def new_f(*args):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(atimeout)
            return f(*args)
            signa.alarm(0)
        new_f.__name__ = f.__name__
        return new_f
    return decorate

@TimeOut(60)
def manage_print():
    print_response = subprocess.Popen('python bin/pure_printer.py '+sys.argv[1], shell=True, stdout=subprocess.PIPE).stdout.read().strip()
    return print_response

# manage pure_printer
try:
    print_output = manage_print()
    output = print_output
except Exception as e:
    output =  "#PRINT_FAIL#"
    subprocess.Popen('for i in `ps aux|grep \'pure_printer.py\'|grep -v \'grep\'| awk \'{ print $2 }\'`; do sudo kill -9 $i; done', shell=True, stdout=subprocess.PIPE).stdout.read()
    os.system('python bin/reset_usb.py \'Seiko\ Epson\ Corp\'')

# check error
if "#PRINT_FAIL#" in output:
	print "found error"
	subprocess.Popen('echo "FAIL,'+str(int(time.time()))+'" > cache/state/printer.csv', shell=True, stdout=subprocess.PIPE)

	# play sound
	os.system('sh ./bin/stopmp3.sh')
	time.sleep(0.2)
	os.system("mpg123 -q ./sounds/th/print-fail.mp3 &")

	# load db print
	file = open("cache/db/"+sys.argv[1], "r")
	obj = json.loads(file.read())

	# api data
	api_url = obj['print_config']+'?key='+obj['print_server_key']
	problem_body = { "problem" : "4" }

	# post problem
	print "post server"
	response = requests.post(
		   api_url,
		   data = json.dumps(problem_body),
		   headers = {'Content-Type': 'application/json'}
	   )
	print response.text
else:
	print "print ok"
	os.system('sudo rm -rf ./cache/db/'+sys.argv[1])
	subprocess.Popen('echo "SUCCESS,'+str(int(time.time()))+'" > cache/state/printer.csv', shell=True, stdout=subprocess.PIPE)

	# play sound
   #os.system('sh ./bin/stopmp3.sh')
   #time.sleep(0.2)
   #os.system("mpg123 -q ./sounds/th/please-pick-slip.mp3 &")

# remove cache
#os.system('sudo rm -rf ./cache/db/'+sys.argv[1])
