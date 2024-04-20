
#from biotech.topics.process_on.p_expect import process_on
from biotech.topics.process_on.p_expect.implicit import process_on_implicit
from biotech.topics.show.variable import show_variable

from biotech.topics.process_on.sub.implicit import process_on_sub_implicit


def dynamic_port (
	process_path = "",
	
	env = "",
	name = ""
):
	script = "python3 " + process_path;
	
	'''
	show_variable ({
		"script:": script,
		"env:": env
	})
	'''

	'''
	the_health_check = process_on_implicit (
		"python3 " + process_path,
		
		#CWD = CWD,
		env = env,
		name = name
	)
	'''
	
	the_health_check = process_on_sub_implicit (
		"python3 " + process_path,
		
		#CWD = CWD,
		env = env
	)
	

	return the_health_check