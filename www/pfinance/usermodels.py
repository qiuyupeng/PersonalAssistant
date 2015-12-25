from .models import *


class holding:
	def __init__(self, history_quote, stock_name):
		self.history_quote = history_quote
		self.latest_quote = history_quote[len(self.history_quote) - 1]

		#quote of the day before latest_quote (defulat to current quote)
		self.pre_quote = self.latest_quote
		for i in range(len(self.history_quote) - 1, -1, -1):
			if self.history_quote[i].update_datetime.date() < self.latest_quote.update_datetime.date():
				self.pre_quote = self.history_quote[i]
				break
		self.price_diff = self.latest_quote.price - self.pre_quote.price
		self.ratio_change = "{0:.2f}%".format(self.price_diff / self.latest_quote.price * 100)

		self.stock_name = stock_name
		#length 3 tuples for each entry: datetime, share, totalcost
		self.buy_seq = [] 
		self.sell_seq = []
		#indicate whether the transaction sequence is sorted 
		self._is_sorted = False

		self.net_share = 0
		self.cost_basis = 0
		self.realized_gain = 0
		self.unrealized_gain = 0

	def put_tran(self, tran):
		"""
		input: tran: userTransaction objects
		will append it to buy_seq or sell_seq depending on the transaction's type
		"""
		self._is_sorted = False

		if tran.tran_type == 'b':
			self.buy_seq.append((tran.exe_datetime, tran.shares, tran.total_cost()))
		else:
			self.sell_seq.append((tran.exe_datetime, tran.shares, tran.total_cost()))

	def _sort_tran(self):
		"""
		sort the buy_seq and sell_seq based on the datetime.
		"""
		if not self._is_sorted:
			self.buy_seq.sort(key = lambda t: t[0])
			self.sell_seq.sort(key = lambda t: t[0])

		self._is_sorted = True

	def calculate_gain(self):
		"""
		Populate the following three entires:
			self.net_share
			self.cost_basis
			self.realized_gain 
			self.unrealized_gain
		"""
		self._sort_tran()

		self.net_share = 0
		self.cost_basis = 0
		self.realized_gain = 0
		self.unrealized_gain = 0

		pos_buy_seq = 0

		total_share_sell = sum([x[1] for x in self.sell_seq])
		total_share_buy = sum(x[1] for x in self.buy_seq)

		self.net_share = total_share_buy - total_share_sell
		self.realized_gain = sum(x[2] for x in self.sell_seq)

		for buy_tran in self.buy_seq:
			if total_share_sell == 0:
				self.cost_basis -= buy_tran[2]
			elif total_share_sell > buy_tran[1]:
				self.realized_gain += buy_tran[2]
				total_share_sell -= buy_tran[1]
			else:
				tmp_gain = buy_tran[2] * total_share_sell / buy_tran[1] 
				total_share_sell = 0

				self.realized_gain += tmp_gain
				self.cost_basis -= (buy_tran[2] - tmp_gain)

		self.unrealized_gain = self.latest_quote.price * self.net_share - self.cost_basis


	def market_value(self):
		"""
		value of current holding
		"""
		return self.latest_quote.price * self.net_share

	def today_gain(self):
		"""
		today's gain or loss
		"""
		return self.net_share * self.price_diff

class portfolio:
	"""
	Info about user's holding and performance
	"""
	def __init__(self, user_obj):
		"""
		Initialize using user_obj
		"""
		self.user_obj = user_obj
		self.transaction_history = userTransaction.objects.filter(user_id=user_obj.id)

		#key: ticker, value: holding obj
		self.holding_dict = {}
		self._construct_holding_dict()


	def _construct_holding_dict(self):
		"""
		This function populates the holding_dict based on self.transaction_history
		and the realized gain.
		"""
		for tran in self.transaction_history:
			if tran.stock_id.ticker_name not in self.holding_dict:
				self.holding_dict[tran.stock_id.ticker_name] = \
					holding(tran.stock_id.all_quote(), tran.stock_id.stock_name)
			self.holding_dict[tran.stock_id.ticker_name].put_tran(tran)

		for ticker_name in self.holding_dict:
			self.holding_dict[ticker_name].calculate_gain()

	def total_realized_gain(self):

		return sum([x.realized_gain for x in self.holding_dict.values()])

	def total_unrealized_gain(self):

		return sum([x.unrealized_gain for x in self.holding_dict.values()])

	def total_cost(self):

		return sum([x.cost_basis for x in self.holding_dict.values()])

	def total_market_value(self):

		return sum([x.market_value() for x in self.holding_dict.values()])

	def total_today_gain(self):

		return sum([x.today_gain() for x in self.holding_dict.values()])









