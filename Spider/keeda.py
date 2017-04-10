from worker import KeedaWorker
from bloomset import BloomSet
from queue import KeedaQueue
import utilities

class Keeda:
	def __init__(self , baseUrl, numthreads=1, depth=1):
			self.baseUrl = baseUrl
			self.numthreads = numthreads
			self.depth = depth
			if not utilities.validateURL(baseUrl):
				raise ValueError("ayuhi ")

	def start(self):
		keedaQueue = KeedaQueue(self.baseUrl, utilities.getDomain(self.baseUrl))
		bloomSet = BloomSet(utilities.getDomain(self.baseUrl))
		for i in range(self.numthreads):
			KeedaWorker(keedaQueue, bloomSet, self.depth)
		keedaQueue.join()
		keedaQueue.close()
		bloomSet.close()
