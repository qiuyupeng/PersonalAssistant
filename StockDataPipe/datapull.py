import urllib2
import json


class baseData:
	"""
	This class pulls data from a given source and return a dictionary object
	"""
	def __init__(self, data_src, frequency, info_type):
		#source of the data, e.g. Google finance
		self.data_src = data_src

		#frequency of pulling data, in second
		self.frequency = frequency

		#data_type: stock data, temperature data
		self.info_type = info_type



url = "http://finance.google.com/finance/info?client=ig&q=NASDAQ:GOOG"

obj = urllib2.urlopen(url)
raw_output = obj.read()
print(raw_output[4:])
x = json.loads(raw_output[4:])
print(x)