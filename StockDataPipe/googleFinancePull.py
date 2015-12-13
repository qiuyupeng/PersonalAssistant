import urllib.request
import json

URL_PREFIX = "http://finance.google.com/finance/info?client=ig&q="

def get_raw_data(list_ticker):

	#construct the query
	final_url = URL_PREFIX + ','.join(list_ticker)
	#fetch data

	with urllib.request.urlopen(final_url) as url_obj:
		str_output = url_obj.read().decode('unicode_escape')

	#the first four chars are redundant
	json_output = json.loads(str_output[4:])

	return json_output



