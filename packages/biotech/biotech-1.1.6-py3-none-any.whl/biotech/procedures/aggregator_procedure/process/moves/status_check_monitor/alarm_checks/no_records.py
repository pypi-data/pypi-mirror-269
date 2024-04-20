
#
#
from biotech.procedures.aggregator_procedure.process.variables import retrieve_variables
from biotech.procedures.aggregator_procedure.process.variables import add_anomaly
#
from biotech.topics.exceptions import parse_exception
#
import time
#
#


'''
	A live process that is indicating that
	it is infinite loop, when it is not.
	
	Therefore if after 5 seconds the records are
	empty, then therer was mostly likely 
	a problem starting the process.

		'scan process venture started': 'yes',
		'scan process started': 'yes',
		'scan process notified aggregator': 'yes',
		'scan process is alive': 'yes',


		'scan process was stopped': 'no',
		'scan returned proceeds': 'no',
		'scan records were retrieved': 'no'
'''
def no_records_check (status_path):
	
	try:	
		aggregator_variables = retrieve_variables ()
		time_limit = aggregator_variables ["intro_variables"] ["time_limit"]
		internal_statuses = aggregator_variables ["internal_statuses"]
		
		status_of_path = internal_statuses [ status_path ]
		occurrences = status_of_path ["occurrences"]
	
		doors = {
			"1": occurrences ["scan process started"] == "yes",
			"2": occurrences ["scan process is alive"] == "yes",
			"3": occurrences ["scan process was stopped"] == "no",
			"4": len (internal_statuses [ status_path ] ["times"] ["venture started"]) >= 1,
			"6": len (internal_statuses [ status_path ] ["records"]) == 0,
			"7": time.time () - float (internal_statuses [ status_path ] ["times"] ["venture started"])
		}
		
	
		if (
			len (internal_statuses [ status_path ] ["times"] ["venture started"]) >= 1 and
			
			occurrences ["scan process started"] == "yes" and
			occurrences ["scan process is alive"] == "yes" and
			occurrences ["scan process notified aggregator"] == "yes" and
			occurrences ["scan process was stopped"] == "no" and
			
			len (internal_statuses [ status_path ] ["records"]) == 0
		):
			elapsed = time.time () - float (internal_statuses [ status_path ] ["times"] ["venture started"]);
		
			if (elapsed >= 15):			
				show_variable ({
					"records were not retrieved after 15 seconds": status_path
				})
				
				try:
					occurrences = internal_statuses [ status_path ] ["occurences"];
				except Exception:
					occurrences = "not found"
				
				aggregator_variables ["internal_statuses"] [ status_path ] ["results_of_scan"] = {
					"path": status_path,
					
					"alarm": "After 15 seconds, no process records were found.",
					"alarm notes": [],
					
					"occurences": occurrences,
					
					"exited": True
				}
			
				aggregator_variables ["internal_statuses"] [ status_path ] ["status"] ["process"] = "done"
				aggregator_variables ["internal_statuses"] [ status_path ] ["process"] ["process"].terminate ()
				
					
	except Exception as E:
		add_anomaly ({
			"anomaly": "physical: process records time limit check exception",
			"status_path": status_path,
			"exception": parse_exception (E1)
		})
