import urlparse

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