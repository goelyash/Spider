import datetime
from Spider import Spider

#Enter base URL, Number of Threads (default=1), Depth of search(default=1)
app = Spider("https://thenewboston.com",8,100)
print datetime.datetime.now()
app.start()
