from worker import SpiderWorker
from bloomset import BloomSet
from queue import SpiderQueue
from storage import Storage
import utilities
import datetime

#Base class for initializing member variables and sending spiderworkers.
class Spider:
	def __init__(self , baseUrl, numthreads=1, depth=1):
			self.baseUrl = baseUrl
			self.numthreads = numthreads
			self.depth = depth
			if not utilities.validateURL(baseUrl):
				raise ValueError("Invalid URL")

	#initialize spiderqueue,bloomset,number of spiderworkers.
	def start(self):
		spiderQueue = SpiderQueue(self.baseUrl, utilities.getDomain(self.baseUrl))
		bloomSet = BloomSet(utilities.getDomain(self.baseUrl))
		for i in range(self.numthreads):
			SpiderWorker(spiderQueue, bloomSet,  self.baseUrl, self.depth)
		spiderQueue.join()
		spiderQueue.close()
		bloomSet.close()
