import urlparse

#validate a given URL. Splits and checks for consistency.
def validateURL(url):
	u = urlparse.urlparse(url)
	if u[0]!='' and u[1]!='':
		return True
	return False

#returns the domain of a URL.
def getDomain(url):
	u = urlparse.urlparse(url)
	return u[1]

#returns the concatination of 2 URL'S
def joinURL(url1,url2):
	return urlparse.urljoin(url1,url2)