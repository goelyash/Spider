import os

#TODO : Check queue count variable. 

class Storage:

	queue = 0
	crawled = 0

	#Initialize member variables
	def __init__(self, name):
		self.name = name
		self.queuePath = os.path.join(name,"queue")
		self.resultsPath = os.path.join(name, "results")
		self.createDirectory()
		self.createFiles()
		self.queueFile
		self.resultsFile
		Storage.queue = 0
		Storage.crawled = 0

	#Creates directory in the name of the base URL
	def createDirectory(self):
		if not os.path.exists(self.name):
			os.makedirs(self.name)
			print("Directory created " + self.name)
		else:
			print("Directory already present")

 	#Creates files required in the directory created above
	def createFiles(self):
		self.queueFile = open(self.queuePath,"a+")
		self.resultsFile = open(self.resultsPath,"a+")

	#Closing files
	def close(self):
		self.queueFile.close()
		self.resultsFile.close()

	#Storing crawled URL's
	def putResult(self,url):
		Storage.crawled = Storage.crawled + 1
		self.resultsFile.write(url+"\n")
		self.resultsFile.flush()

	def putResults(self, urls):
		for url in urls:
			self.resultsFile.write(url+"\n")
			Storage.crawled = Storage.crawled + 1

	#Stroring URL's in the queue file
	def putQueues(self, urls, depth=0):
		for url in urls:
			self.queueFile.write(url+" "+str(depth)+"\n")
			Storage.queue = Storage.queue + 1

	def putQueue(self, url, depth=0):
		Storage.queue = Storage.queue + 1
		self.queueFile.write(url+" "+str(depth)+"\n")
		

	#Returning top 'n' URL's from the queue file
	def topQueue(self, n=0):
		self.queueFile.seek(0)
		lines = self.queueFile.read().splitlines()
		if n==0:
			return lines
		return lines[:n]

	#Removing top 'n' URL's from the queue file 
	def popQueue(self, n):
		self.queueFile.seek(0)
		lines = self.queueFile.readlines()
		self.queueFile.seek(0)
		self.queueFile.truncate()
		for i in range(n, len(lines)):
			self.queueFile.write(lines[i])