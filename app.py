import datetime
from Spider import Spider

#Enter base URL, Number of Threads (default=1), Depth of search(default=1)
app = Spider("http://results.vtu.ac.in",4,4)
print datetime.datetime.now()
app.start()
