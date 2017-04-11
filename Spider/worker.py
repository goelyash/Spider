from urllib2 import urlopen
from HTMLParser import HTMLParser
from queue import SpiderQueue
from bloomset import BloomSet
from threading import Thread
import utilities

#Class for Crawling URL's
class SpiderWorker(HTMLParser):

 	#initialize members.
	def __init__(self, queue, bloomset, maxDepth=1):
		HTMLParser.__init__(self)
		self.queue = queue
		self.bloomset = bloomset
		self.maxDepth = maxDepth
		self.urls = []
		self.currentUrl = ''
		t = Thread(target=self.crawl)
		t.daemon = True
		t.start()

	#Identifies anchor tag's from the HTML code 
	def handle_starttag(self, tag, attrs):
		temp = ''
		if tag == 'a':
			for (attribute, value) in attrs:
				if attribute == 'href':
					if utilities.validateURL(value):
						temp = value
					else:
						temp = (utilities.joinURL(self.url,value))
					try:
						temp = temp.decode('utf-8')
					except:
						return
					self.urls.append(temp)

	'''
	Check's the depth of link to be crawled
	Takes the HTML code of the page, decodes it and calls the above function
	Places the new URL's in the queue file
	Places the crawled URL in the result file and bloomset 
	Once crawled until the required depth returns back to spider.py
	'''
	def crawl(self):
		while True:
			try:
				self.urls = []
				line = self.queue.get()
				self.url,depth = line
				depth = int(depth)
				if depth>=self.maxDepth or self.bloomset.get(self.url):
					continue
				self.bloomset.add(self.url)
				res = urlopen(self.url)
				body = res.read().decode("ISO-8859-1")
				self.feed(body)
				print self.url,len(self.urls)
				self.queue.put(self.urls, depth+1)
				self.queue.putResult(self.url)
			except Exception as e:
				print e,line
			finally:
				self.queue.task_done()
