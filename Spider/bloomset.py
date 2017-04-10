from pybloom import ScalableBloomFilter
from os import path
from threading import Lock

MAX_BUF_WRITES = 10

#BloomSet is used to maintain visited status of the urls
class BloomSet:

	#initialize member variables
	def __init__(self, name):
		self.name = name
		self.lock = Lock()
		self.writes = 0
		self.file = open(path.join(self.name,"bloom"), "a+")
		self.filter = self.boot()

	def __contains__(self, val):
		return val in self.filter

	def add(self,arg):
		self.lock.acquire()
		self.filter.add(arg)
		self.writes+=1
		if self.writes > MAX_BUF_WRITES:
			self.writes -=MAX_BUF_WRITES
			self.write()
		self.lock.release()

	def get(self, arg):
		return arg in self.filter

	def boot(self):
		try:
			self.file.seek(0)
			a = ScalableBloomFilter.fromfile(self.file)
			return a
		except:
			return ScalableBloomFilter(ScalableBloomFilter.LARGE_SET_GROWTH)

	def write(self):
		self.file.seek(0)
		self.file.truncate()
		self.filter.tofile(self.file)

	def close(self):
		self.filter.tofile(self.file)
		self.file.close()

