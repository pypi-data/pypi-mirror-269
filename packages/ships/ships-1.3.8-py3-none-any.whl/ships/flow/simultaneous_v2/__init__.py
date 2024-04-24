




'''
	from ships.flow.simultaneous_v2 import simultaneously_v2
	
	import time
	
	def move (item):
		print ("starting", item)
		
		time.sleep (item)
		result = f"Processed item: {item}"
		print (result)
		
		return result


	proceeds = simultaneously_v2 (
		items = [3.5, 1, 2, 1.1, 4, 1.11, 1.12, 1.13],
		capacity = 4,
		move = move
	)
'''

'''
	#
	#	This contains the indexes of the anomalies
	#	
	#
	proceeds ["anomalies"]
'''

'''
	#
	#	This contains the results
	#	
	#
	proceeds ["results"]
	
		[
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


import threading
from queue import Queue
import time

import ships.modules.exceptions.parse as parse_exception
def simultaneously_v2 (
	items = [],
	capacity = 2,
	move = lambda : None
):
	#
	#	capacity = 2
	#
	semaphore = threading.Semaphore (capacity)

	anomalies = []

	# Define a function to process items with semaphore limit and return results
	def process_with_semaphore (item, index, results_queue, anomalies_queue):
		nonlocal anomalies;
	
		with semaphore:
			exception = ""
			result = ""
			anomaly = "no"
		
			try:
				proceeds = move (item)
			except Exception as E:
				print ("exception:", E)
				
				exception = parse_exception.now (E)
				anomaly = "yes"
				result = ""
				
				anomalies_queue.put (index)
			
				proceeds = {
					"result": result,
					"anomaly": anomaly,
					"exception": exception
				}
			
			
			
			
			#
			#  place the result along with its index in the queue
			#
			results_queue.put ((index, proceeds))

	#
	#	create a queue to collect the results
	#
	#
	results_queue = Queue ()
	anomalies_queue = Queue ()

	#
	#	create threads to process items
	#
	#
	threads = []
	for index, item in enumerate (items):
		thread = threading.Thread (
			target = process_with_semaphore, 
			args = (item, index, results_queue, anomalies_queue)
		)
		
		thread.start ()
		threads.append (thread)


	for thread in threads:
		thread.join ()

	#
	#	collect results from the queue and reorder them based on the original item order
	#
	#
	results = [None] * len (items)
	while not results_queue.empty ():
		index, result = results_queue.get ()
		results [index] = result
		
	anomalies_list = []
	while not anomalies_queue.empty():
		anomalies_list.append (anomalies_queue.get ())
	
	
	return {
		"results": results,
		"anomalies": anomalies_list
	};