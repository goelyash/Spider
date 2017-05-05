import urlparse
import csv

#validate a given URL
def validateURL(url):
	u = urlparse.urlparse(url)
	if u[0]!='' and u[1]!='':
		return True
	return False

#Returns domain of a URL
def getDomain(url):
	u = urlparse.urlparse(url)
	return u[1]

#Concatinates 2 URL's
def joinURL(url1,url2):
	return urlparse.urljoin(url1,url2)

'''
compares 2 URL's for exact same domain
If URL's aren't same then return True
'''
def compare(baseURL, crawlURL):
	baseDomain = getDomain(baseURL)
	crawlDomain = getDomain(crawlURL)
	if baseDomain == crawlDomain:
		return False
	for i in range(1):
		if baseDomain[0] != 'w' and baseDomain[1] != 'w' and baseDomain[2] != 'w' and baseDomain[3] != '.' :
			baseDomain = "www." + baseDomain
		if crawlDomain[0] != 'w' and crawlDomain[1] != 'w' and crawlDomain[2] != 'w' and crawlDomain[3] != '.' :
			crawlDomain = "www." + crawlDomain
		if baseDomain == crawlDomain:
			return False
	return True

def split(url):
	parsedURL = urlparse.urlparse(url)
	path = parsedURL[2]
	splitList = path.split('/')
	return splitList

def addtocsv(t,q,c):
	with open('linkrate.csv','a') as newFile:
		newFileWriter = csv.writer(newFile)
		newFileWriter.writerow([t,q,c])
