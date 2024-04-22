

import shlex
import subprocess
import atexit

def process_on_sub_implicit (
	command, 
	
	CWD = None, 
	env = None
):

	print ("process_on_sub_implicit")

	command = shlex.split (command)

	implicit_process = subprocess.Popen (
	#process = subprocess.call (
	
		command, 
		
		cwd = CWD, 
		env = env, 
		
		#
		#	similar to stdbuf -o0
		#
		# bufsize = 0,
		
		#shell = True
		
		#stdout = subprocess.PIPE, 
		#stderr = subprocess.PIPE
	)
	
	def stop ():
		nonlocal implicit_process;	
		#venture ["process"].terminate ()
		implicit_process.kill ()
		#os.kill (venture ["process"].pid, signal.SIGINT)

	def is_going ():
		nonlocal implicit_process;
		
		try:
			if (implicit_process.poll () == None):
				return "yes"
			
			return "no"
		
		except Exception:
			print ("exception:", E)
			
		return "unknown"

	atexit.register (stop)

	#
	#	don't worry about this one
	#
	def records ():
		return []

	return {
		"process": implicit_process,
		"records": records,
		
		"stop": stop,
		"is_going": is_going
	}



