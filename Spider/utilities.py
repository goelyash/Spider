import urlparse

def validateURL(url):
	u = urlparse.urlparse(url)
	if u[0]!='' and u[1]!='':
		return True
	return False

def getDomain(url):
	u = urlparse.urlparse(url)
	return u[1]

def joinURL(url1,url2):
	return urlparse.urljoin(url1,url2)