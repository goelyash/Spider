from Queue import Queue
from storage import Storage
from threading import Lock

MAX_BACKLOG = 100
MAX_QUEUE_SIZE = 100
MIN_QUEUE_SIZE = 2

class KeedaQueue(Queue):

	def __init__(self, url, name="default"):
		Queue.__init__(self)
		self.storage = Storage(name)
		self.storage.putQueue(url)
		self.readCount = 0
		self.lock = Lock()
		self.loadFromStorage()

	#retrives max_backlog urls from storage queue
	def loadFromStorage(self):
		urls = self.storage.topQueue(MAX_QUEUE_SIZE)
		for url in urls:
			Queue.put(self, url)

	def put(self,urls, depth=0):
		self.lock.acquire()
		self.storage.putQueues(urls, depth)
		if self.qsize()==0:
			self.loadFromStorage()
		self.lock.release()

	def putResult(self, url):
		self.lock.acquire()
		self.storage.putResult(url)
		self.lock.release()

	def get(self):
		#if the queue is empty then load from storage
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
			self.storage.popQueue(MAX_BACKLOG)
		self.lock.release()
		return element.split(' ')

	def close(self):
		self.lock.acquire()
		self.storage.popQueue(self.readCount)
		self.storage.close()
		self.lock.release()