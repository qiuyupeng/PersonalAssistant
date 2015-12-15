import urllib.request
import json
import decimal
import datetime
from pytz import timezone
decimal.getcontext().prec = 2

from .dbproxy import dbProxy


URL_PREFIX = "http://finance.google.com/finance/info?client=ig&q="


class stockPriceWritter:

	def __init__(self):

		self._db_proxy = dbProxy()

	def query(self):
		"""
		The main API that pulls data and writes to db
		"""
		#get list of ticker
		ticker_id_dict = self.get_list_ticker()

		quote_dict = self.get_quote(ticker_id_dict.keys())

		self.clean_stale_quote(quote_dict)
		self._write_quote_to_db(ticker_id_dict, quote_dict)

	def clean_stale_quote(self, quote_dict):
		"""
		When the stock market closes, the quote is the stale one and we do not
		store those info in the db. (stale quote is defined as 10 mins latency)
		This function remove all the stale quote
		"""
		list_stale_quote = []

		last_quote_time_dict = self.get_latest_update()
		delta = datetime.timedelta(minutes=10)
		for q in quote_dict:
			if (q in last_quote_time_dict) and quote_dict[q]['dt'] - delta < last_quote_time_dict[q]:
				list_stale_quote.append(q)

		for q in list_stale_quote:
			del quote_dict[q]

	def get_list_ticker(self):
		"""
		let ticker lists that needs quote

		Return dict:
			key: ticker_name
			value: id in the database table
		"""
		sql_query = "SELECT id, ticker_name FROM pfinance_staticstockinfo"
	
		id_ticker_pair_list = self._db_proxy.get_result(sql_query)
	
		output_dict = {}
		for id_ticker_pair in id_ticker_pair_list:
			output_dict[id_ticker_pair[1]] = id_ticker_pair[0]

		return output_dict 

	def get_quote(self, list_ticker):
		"""
		return dictionary of the requested quote
		"""
		try:
			raw_quote = self.get_raw_data_from_gfinance(list_ticker)
		except urllib.error.URLError:
			"""
			The query fails
			"""
			#TODO: log the failure
			return {}

		quote_dict = {}
		for q in raw_quote:
			ticker = q['e'] + ":" + q['t']
		
			dt_wotzinfo = datetime.datetime.strptime(q['lt_dts'], '%Y-%m-%dT%H:%M:%SZ')
		
			quote_dict[ticker] = {
				'dt': dt_wotzinfo.replace(tzinfo=timezone('EST')),
				'price': decimal.Decimal(q['l']),
			}

		return quote_dict

	def get_raw_data_from_gfinance(self, list_ticker):
		"""
		query the Google Finance API
		"""
		#construct the query
		final_url = URL_PREFIX + ','.join(list_ticker)
		#fetch data

		with urllib.request.urlopen(final_url) as url_obj:
			str_output = url_obj.read().decode('unicode_escape')

		#the first four chars are redundant
		json_output = json.loads(str_output[4:])

		return json_output

	def _write_quote_to_db(self, ticker_id_dict, quote_dict):
		"""
		write to table pfinance_stockprice
		"""

		for ticker_id in quote_dict:

			sql_query = """INSERT INTO pfinance_stockprice 
				(update_datetime, price, stock_id_id)
				VALUES ('{0}', {1}, {2})
			""".format(quote_dict[ticker_id]['dt'], quote_dict[ticker_id]['price'], 
				ticker_id_dict[ticker_id])

			self._db_proxy.write_result(sql_query)

	def get_latest_update(self):
		"""
		get the time of the last update, a datetime obj
		"""
		sql_query = """SELECT MAX(pfinance_stockprice.update_datetime), pfinance_staticstockinfo.ticker_name 
			FROM pfinance_stockprice 
			INNER JOIN pfinance_staticstockinfo
			ON pfinance_staticstockinfo.id=pfinance_stockprice.stock_id_id
			GROUP BY pfinance_staticstockinfo.id
		"""
		raw_result = self._db_proxy.get_result(sql_query)

		output_dict = {}
		for row in raw_result:
			output_dict[row[1]] = row[0]

		return output_dict
