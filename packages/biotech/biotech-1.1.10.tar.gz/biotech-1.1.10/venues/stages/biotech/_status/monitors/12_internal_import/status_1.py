
'''
	python3 /biotech/venues/stages/biotech/_status/status.proc.py "12_internal_import/status_1.py"
'''

'''
	netstat -tuln | grep 52435
'''

import pathlib
from os.path import dirname, join, normpath
import biotech

import time
import rich

def check_1 ():
	this_directory = pathlib.Path (__file__).parent.resolve ()
	this_module = str (this_directory)
	the_guarantees = str (normpath (join (this_directory, f"guarantees")))
	
	relative_path = str (normpath (join (this_directory, f"..")))
	
	bio = biotech.on ({
		"glob_string": this_module + "/**/guarantee_*.py",
		
		"simultaneous": True,
		"simultaneous_capacity": 10,

		"module_paths": [],

		"relative_path": relative_path,
		
		"aggregation_format": 2
	})
	
	bio ["off"] ()
	scan = bio ["proceeds"]


	#time.sleep (5)

	
	#time.sleep (5)

	assert (scan ["stats"] ["paths"] ["alarms"] == 1), scan ["stats"]
	assert (scan ["stats"] ["paths"] ["empty"] == 0), scan ["stats"]

	assert (scan ["stats"] ["checks"] ["passes"] == 0), scan ["stats"]
	assert (scan ["stats"] ["checks"] ["alarms"] == 0), scan ["stats"]
	
checks = {
	'internal import not possible': check_1
}
