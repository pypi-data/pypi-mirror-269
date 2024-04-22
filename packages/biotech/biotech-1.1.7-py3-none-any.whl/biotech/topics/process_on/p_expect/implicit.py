
'''
	from biotech.topics.process_on.p_expect.implicit import process_on_implicit
	
	venture = process_on_implicit (
		'python3 server.py',
		
		CWD = None,
		env = {}
	)
	venture ["process"].terminate ()
	
	#
	# status
	#
	#
	print ('status:', venture ["process"].is_alive ())
	
	#
	#	stop the process
	#
	#
	
	records = venture ["records"] ()
'''

from biotech.topics.process_on.p_expect import process_on

import pexpect
import rich

import os
from multiprocessing import Process, Queue
import multiprocessing
import atexit
import time

def off (implicit_process):
	try:
		print ("""
		
			attemping to stop the implicit venture
		
		""")
		implicit_process.terminate ()
	except Exception as E:
		print ("venture implicit off exception:", E)
	
		pass;

def process_on_implicit (
	process_string,
	
	the_queue = None,
	CWD = None,
	env = {},
	
	name = "process"
):
	the_queue = Queue ()

	stop_event = multiprocessing.Event ()

	implicit_process = Process (
		target = process_on,
		
		args = [ 
			process_string 
		],
		
		kwargs = {
			"the_queue": the_queue,
			"CWD": CWD,
			"env": env,
			"name": name,
			
			"stop_event": stop_event
		}
	)
	
	implicit_process.start ()
	
	# if you'd like to await the process
	# implicit_process.join ()
	
	
	def parse_queue ():
		proceeds = []
		while not the_queue.empty ():
			proceeds.append (the_queue.get ())
	
		return proceeds;
	
	def is_going ():
		nonlocal implicit_process;
		
		try:
			if (implicit_process.is_alive () == True):
				return "yes"
			
			return "no"
		
		except Exception:
			print ("exception:", E)
			
		return "unknown"
	
	def stop ():
		nonlocal implicit_process;
		
		implicit_process.terminate ();
		
		while is_going () == "yes":
			time.sleep (.1)
	
		#nonlocal stop_event;
		#stop_event.set ()
	
	atexit.register (stop)
	
	return {
		"process": implicit_process,
		"records": parse_queue,
		
		#
		#	This might not do anything
		#
		"stop": stop,
		"is_going": is_going
	}
	
	