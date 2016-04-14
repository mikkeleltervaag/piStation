# My imports
from settings import *

def getBrentCrude():
	try:
		urlStr = "http://www.bloomberg.com/quote/CO1:COM"

		fileObj = urllib.urlopen(urlStr)

		for line in fileObj:
		    if ('<div class="price">' in line):   
			    startIndex = line.find('<div class="price">') + 19
			    endIndex = line.find('</div>',startIndex)
			    return line[startIndex:endIndex]
	except:
		print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " Cannot get Brent Crude Price"
	else:
		return "none"