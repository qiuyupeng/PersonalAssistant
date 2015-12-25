from django.db import models
import datetime
from pytz import timezone
# Create your models here.

class staticStockInfo(models.Model):
	STOCK_TYPE = (
		('i', 'institution'),
		('e', 'ETF'),
		('m', 'Mutual Fund')
	)

	stock_name = models.CharField(max_length = 128)
	exchange_name = models.CharField(max_length = 32)
	ticker_name = models.CharField(max_length = 32)
	s_type = models.CharField(max_length=1, choices=STOCK_TYPE)

	def __str__(self):
		return self.ticker_name

	def all_quote(self, starting_datetime=None):
		"""
		get all quotes about the stock, after starting time.
		If starting time is None, using 1year by default.
		"""
		now = datetime.datetime.now(tz=timezone('EST'))

		if starting_datetime is None:
			starting_datetime = now - datetime.timedelta(days=365)

		return self.stockprice_set.filter(update_datetime__gte=starting_datetime).order_by('update_datetime')

	def latest_quote(self):
		"""
		get the latest quote from the database
		"""
		latest_datetime = self.stockprice_set.aggregate(
			models.Max('update_datetime'))['update_datetime__max']

		return self.stockprice_set.get(update_datetime=latest_datetime)



class userInfo(models.Model):

	last_name = models.CharField(max_length=32)
	first_name = models.CharField(max_length=32)

	login_username = models.CharField(max_length=32)
	login_password = models.CharField(max_length=256)

	def __str__(self):
		return self.last_name + ',' + self.first_name


class stockPrice(models.Model):
	stock_id = models.ForeignKey(staticStockInfo, on_delete=models.CASCADE)

	update_datetime = models.DateTimeField('date/time published')
	price = models.DecimalField(max_digits=10, decimal_places=2)


class userTransaction(models.Model):
	TRANSACTION_TYPE = (
		('b', 'BUY'),
		('s', 'SELL')
	)

	stock_id = models.ForeignKey(staticStockInfo, on_delete=models.CASCADE)
	user_id = models.ForeignKey(userInfo, on_delete=models.CASCADE)

	exe_datetime = models.DateTimeField('date/time published')
	tran_type = models.CharField(max_length=1, choices=TRANSACTION_TYPE)
	shares = models.PositiveIntegerField()
	price = models.DecimalField(max_digits=10, decimal_places=2)
	commission = models.DecimalField(max_digits=5, decimal_places=2)

	def __str__(self):
		output = str(self.user_id) + ' {0} ' + str(self.stock_id)
		if (self.tran_type == 'b'):
			return output.format('buy')
		else:
			return output.format('sell')

	def total_cost(self):
		"""
		Calculate the cost of the transaction, sell is positive, buy is negative
		"""
		if self.tran_type == 'b':
			return - self.shares * self.price - self.commission
		else:
			return self.shares * self.price - self.commission




