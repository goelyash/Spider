from pybloom import ScalableBloomFilter
import os
from threading import Lock

MAX_BUF_WRITES = 10

#BloomSet is used to maintain visited status of the urls
class BloomSet:

	#initialize member variables
	def __init__(self, name):
		self.name = name
		self.multiDir = "MultiBloom"
		self.multiName = "bloom"
		self.lock = Lock()
		self.writes = 0
		self.multiFiles = 0
		#self.file = open(os.path.join(self.name,"bloom"), "a+")
		os.chdir(self.name)
		self.file = open("bloom", "a+")
		if not os.path.exists("MultiBloom"):
			print("Directory created MultiBloom")
			os.makedirs("MultiBloom")
		else:
			print("Directory already present")
		self.filter = self.boot()

#create a file for every depth of a link
#Remove self.file during initialization and add a file initialization for every depth 
#thats crawled by taking the depth as argument.

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

	def multiAdd(self,urls):
		self.lock.acquire()
		for i in range(0, len(urls)):
			if urls[i] == "":
				pass
			else:
				filename = self.multiName + str(i)
				self.multiFile = open(os.path.join(self.multiDir,filename), "a")
				self.filter1 = self.boot1()
				self.multiFile.seek(0)
				self.multiFile.truncate()
				self.filter1.add(urls[i])
				self.filter1.tofile(self.multiFile)
				self.multiFile.close()
		self.lock.release()

	def boot1(self):
		try:
			self.multiFile.seek(0)
			a = ScalableBloomFilter.fromfile(self.multiFile)
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

