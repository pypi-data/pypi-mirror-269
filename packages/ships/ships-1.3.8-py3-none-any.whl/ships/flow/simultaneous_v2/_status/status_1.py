







'''
	cd /ships/fields/gardens/ships/_status/
	python3 status.proc.py "flow/simultaneous_v2/_status/status_1.py"
'''

from ships.flow.simultaneous_v2 import simultaneously_v2

import rich

import time
import atexit
import shlex
import subprocess


	
def check_1 ():
	def move (item):
		if (item == 1):
			raise Exception ("exception!")
	
		return item + 1


	'''
		results = [
			4.5,
			{
				"result": "",
				"anomaly": "yes",
				"exception": ""
			},
			3,
			2.1,
			5,
			2.11,
			2.12,
			2.13
		]
	'''
	
	'''
		anomalies = [ 2 ]
	'''
	items = [ 3.5, 1, 2, 1.1, 4, 1.11, 1.12, 1.13 ]
	proceeds = simultaneously_v2 (
		items = items,
		capacity = 4,
		move = move
	)

	rich.print_json (data = {
		"sim proceeds": proceeds
	})
	
	anomalies = proceeds ["anomalies"]
	results = proceeds ["results"]
	
	assert (anomalies == [ 1 ])

	index = 0
	for result in results:
		if (index not in anomalies):
			assert (results [index] == items [index] + 1), [ 
				index, 
				results [index], 
				items [index]
			]


	#results = proceeds ["results"]
	#anomalies = proceeds ["anomalies"]

	#print ("sim proceeds:", proceeds)
	
checks = {
	"check 1": check_1
}