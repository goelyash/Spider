import os

class Storage:

#initialize member variables.
	def __init__(self, name):
		self.name = name
		self.queuePath = os.path.join(name,"queue")
		self.resultsPath = os.path.join(name, "results")
		self.createDirectory()
		self.createFiles()
		self.queueFile
		self.resultsFile

	#Creating a directory for a specific base URL
	def createDirectory(self):
		if not os.path.exists(self.name):
			os.makedirs(self.name)
			print("directory created " + self.name)
		else:
			print("Directory already present")
 	
 	#create  the files for the above directory.
	def createFiles(self):
		self.queueFile = open(self.queuePath,"a+")
		self.resultsFile = open(self.resultsPath,"a+")

	#close the files after use.
	def close(self):
		self.queueFile.close()
		self.resultsFile.close()

	def putResult(self,url):
		self.resultsFile.write(url+"\n")
		self.resultsFile.flush()

	def putResults(self, urls):
		for url in urls:
			self.resultsFile.write(url+"\n")

	def putQueues(self, urls, depth=0):
		for url in urls:
			self.queueFile.write(url+" "+str(depth)+"\n")

	def putQueue(self, url, depth=0):
		self.queueFile.write(url+" "+str(depth)+"\n")

	def topQueue(self, n=0):
		self.queueFile.seek(0)
		lines = self.queueFile.read().splitlines()
		if n==0:
			return lines
		return lines[:n]

	def popQueue(self, n):
		self.queueFile.seek(0)
		lines = self.queueFile.readlines()
		self.queueFile.seek(0)
		self.queueFile.truncate()
		for i in range(n, len(lines)):
			self.queueFile.write(lines[i]) 

		