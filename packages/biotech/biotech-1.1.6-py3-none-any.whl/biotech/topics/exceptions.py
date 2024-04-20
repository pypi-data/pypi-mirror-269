

'''
import biotech.topics.exceptions as bs_exceptions
'''

'''
from biotech.topics.exceptions import parse_exception
'''

import io
import sys
import traceback
def find_trace (exception : Exception) -> str:
	try:
		file = io.StringIO ()
		traceback.print_exception (exception, file = file)
		
		#return traceback.format_stack()
		
		return file.getvalue ().rstrip ().split ("\n")
	except Exception:
		pass;
		
	return 'An exception occurred while calculating trace.'
	
	
def parse_exception (e):
	try:	
		# Format the exception message with traceback
		exception_message = traceback.format_exception(type(e), e, e.__traceback__)
		return "".join(exception_message)
		
	except Exception:
		print ("couldn't parse exception")
		
	return 'could not parse exception'