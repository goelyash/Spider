from Queue import Queue
from storage import Storage
from threading import Lock

MAX_BACKLOG = 100
MAX_QUEUE_SIZE = 100
MIN_QUEUE_SIZE = 2

class SpiderQueue(Queue):

	def __init__(self, url, name="default"):
		Queue.__init__(self)
		self.storage = Storage(name)
		self.storage.putQueue(url)
		self.readCount = 0
		self.lock = Lock()
		self.loadFromStorage()

	#Retrives max_backlog urls from storage queue
	def loadFromStorage(self):
		urls = self.storage.topQueue(MAX_QUEUE_SIZE)
		for url in urls:
			Queue.put(self, url)

	'''
	Store's the recieved URL's in the Queue File
	If found empty then loads it again from storage queue	
	''' 
	def put(self,urls, depth=0):
		self.lock.acquire()
		self.storage.putQueues(urls, depth)
		if self.qsize()==0:
			self.loadFromStorage()
		self.lock.release()

	#Stores the crawled links in the Result file
	def putResult(self, url):
		self.lock.acquire()
		self.storage.putResult(url)
		self.lock.release()


	'''
	Returns MAX_QUEUE_SIZE URL's to the specific thread
	If file found empty then Reloads it from storage
	'''
	def get(self):
		if self.qsize()==0:
			self.lock.acquire()
			if self.qsize()==0:
				self.storage.popQueue(self.readCount)
				self.readCount = 0
				self.loadFromStorage()
			self.lock.release()
		element  = Queue.get(self)
		self.lock.acquire()
		self.readCount+=1
		if self.readCount>MAX_BACKLOG:
			self.readCount-=MAX_BACKLOG
			self.storage.popQueue(MAX_QUEUE_SIZE)
		self.lock.release()
		return element.split(' ')

	#Closes Storage file
	def close(self):
		self.lock.acquire()
		self.storage.popQueue(self.readCount)
		self.storage.close()
		self.lock.release()