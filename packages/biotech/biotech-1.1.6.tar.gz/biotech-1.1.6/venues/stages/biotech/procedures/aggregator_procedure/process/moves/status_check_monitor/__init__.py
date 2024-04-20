

'''
	the_scan ["process"].is_alive ()
'''


#----
#
from biotech.procedures.aggregator_procedure.process.variables import aggregator_variables
#	
from ..aggregate_stats import aggregate_stats
from ..done_with_scan import done_with_scan_move
#
from .the_physical import parse_and_check_is_alive_of_statuses
from .send_done_if_finished import send_done_if_finished
#
from biotech.topics.implicit.thread import implicit_thread
from biotech.topics.process_on.p_expect.parse_records import parse_p_expect_records
from biotech.topics.show.variable import show_variable
#
from biotech.procedures.aggregator_procedure.process.variables import add_anomaly
from biotech.topics.exceptions import parse_exception
	
#
#
import rich
#
#
import time
import traceback
#
#----


def print_waiting_for (unfinished_scans, time_limit):
	report = []
	
	for unfinished_scan in unfinished_scans:
		internals = unfinished_scan ["internals"]
	
		report.append ({
			"path": unfinished_scan ["path"],
			"internals": internals
		})
		
	show_variable ({
		"time_limit": time_limit,
		"waiting for:": report
	}, mode = "show")



def status_check_monitor ():
	details = aggregator_variables ["details"]

	def task (stop_event = None):		
		cycle = 1
	
		while not stop_event.is_set ():
			time_limit = "unknown"
			
			try:
				if ("time_limit" in aggregator_variables ["intro_variables"]):
					time_limit = aggregator_variables ["intro_variables"] ["time_limit"]
			except Exception as E:
				add_anomaly ({
					"anomaly": "time limit lookup exception",
					"exception": parse_exception (E)
				})
		
			
			#
			# check if internal_statuses_built
			#
			#
			try:
				if (aggregator_variables ["internal_statuses_built"] != "yes"):
					continue;
			except Exception as E:
				add_anomaly ({
					"anomaly": "internal_statuses_built lookup exception",
					"exception": parse_exception (E)
				})
			
			try:
				unfinished = parse_and_check_is_alive_of_statuses ()
			
				if (cycle == 0):
					print_waiting_for (unfinished, time_limit)
				
				result = send_done_if_finished (unfinished)
				if (result == "sent"):
					break;
			except Exception as E:
				add_anomaly ({
					"anomaly": "Could not calculate what paths aren't finished.",
					"exception": parse_exception (E)
				})
			
			cycle += 1
			if (cycle == 3):
				cycle = 0
			
			time.sleep (1)
			



	the_task = implicit_thread (
		task = task
	)
	the_task ['on'] ()
	
	# the_task ['on'] ()
	