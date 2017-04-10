import datetime
from Spider import Spider

app = Spider("http://www.news.google.com",4,4)
print datetime.datetime.now()
app.start()
