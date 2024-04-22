
'''
	from biotech.topics.show.variable import show_variable
	show_variable ()
'''

'''
	{
		"line": 
		"file": 
	}
'''

#----
#
import inspect
from pprint import pprint
import sys
import traceback
#
#----

def show_variable (variable, mode = ""):
	try:
		filename = "?"
		lineno = "?"
		try:
			raise Exception ()
		except:
			exc_type, exc_value, exc_traceback = sys.exc_info ()
			
			try:
				filename = exc_traceback.tb_frame.f_back.f_code.co_filename
			except Exception:
				pass;
				
			try:
				lineno = exc_traceback.tb_frame.f_back.f_lineno
			except Exception:
				pass;

		
		if (mode == "condensed"):
			console = Console()
			
			with console.capture () as capture:
				console.print (variable, end = "")

			output_string = capture.get()

			
			print (f"{ filename }:{ lineno }: " + output_string)
			
		else:
			pprint ({
				"variable": variable,
				"path": filename,
				"line": lineno,
			})
			
	except Exception as E:
		print ("variable printing exception:", E)