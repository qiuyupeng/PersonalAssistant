import unittest
import urllib.request

from .googleFinancePull import get_raw_data

class TestGoogleFinance(unittest.TestCase):
	"""
	This class tests the GoogleFinancePull.py 
	"""
	def getTestCaseNames(self):
		return ('test_oneticker')
	def test_oneticker(self):
		"""
		Test whether the get_raw_data function returns the result ticker of NASDQ:GOOG
		"""
		try:
			data = get_raw_data(["NASDQ:GOOG"])
		except urllib.error.URLError as e:
			#bad request
			self.assertNotEqual(e.reason, 'Bad Request')
			#other error may be caused by no internet connection
		else:
			self.assertEqual('GOOG',data[0]['t'])

	def test_mutlipletickers(self):
		"""
		Test whether the get_raw_data function returns the result ticker of NASDQ:GOOG
		"""
		try:
			data = get_raw_data(["NASDQ:GOOG", "NASDQ:FB"])
		except urllib.error.URLError as e:
			#bad request
			self.assertNotEqual(e.reason, 'Bad Request')
			#other error may be caused by no internet connection
		else:
			self.assertEqual('GOOG', data[0]['t'])
			self.assertEqual('FB', data[1]['t'])
