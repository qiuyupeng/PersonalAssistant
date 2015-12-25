import datetime
from pytz import timezone

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods

from .models import userInfo, userTransaction, staticStockInfo
from .usermodels import portfolio

CLIENT_ID = 'client_id'


def login(request):

	if CLIENT_ID in request.session:
		return detail_user(request)
	else:
		return render(request, 'pfinance/user_login.html')

def detail_user(request):
	"""
	display users info
	"""
	#verify login
	if CLIENT_ID not in request.session:
		return HttpResponseRedirect(reverse('pfinance:login'))

	try:
		user_obj = userInfo.objects.get(pk=request.session[CLIENT_ID])
	except userInfo.DoesNotExist:
		return HttpResponseRedirect(reverse('pfinance:logout'))

	user_portfolio = portfolio(user_obj)

	transaction_history = userTransaction.objects.filter(user_id=user_obj.id)
	
	return render(request, 'pfinance/detail_userinfo.html', {
			'user_obj': user_obj,
			'transaction_history': transaction_history,
			'user_portfolio': user_portfolio,
		})


@require_http_methods(["POST"])
def login_verify(request):
	"""
	verify whether user is legitimate 
	"""
	if CLIENT_ID not in request.session:
		try:
			client_usr = request.POST['usr']
			client_pwd = request.POST['pwd']
			client_obj = userInfo.objects.get(login_username=client_usr,login_password=client_pwd)
		except userInfo.DoesNotExist:
			return HttpResponse("Login Failed")
		request.session[CLIENT_ID] = client_obj.id

	return HttpResponseRedirect(reverse('pfinance:login'))

		
def logout(request):
	"""
	logout a user, redirect to the login page
	"""
	request.session.flush()

	return HttpResponseRedirect(reverse('pfinance:login'))

@require_http_methods(["POST"])	
def add_tran(request):
	"""
	add a transaction to a user
	"""
	if CLIENT_ID in request.session:
		#TODO CHECK If all entries are valid
		try:
			stock_obj = staticStockInfo.objects.get(
				ticker_name=request.POST['ticker'].upper())

			user_obj = userInfo.objects.get(pk=request.session[CLIENT_ID])

			trade_date_obj = datetime.datetime.strptime(request.POST['trade_date'],'%m/%d/%Y')
			trade_date_obj = trade_date_obj.replace(
				hour = 12,
				minute = 0,
				second = 0,
				tzinfo=timezone('EST'),)
			print(trade_date_obj)
			usr_tran_obj = userTransaction(
					stock_id=stock_obj,
					user_id=user_obj,
					exe_datetime=trade_date_obj,
					tran_type=request.POST['tran_type'],
					shares=int(request.POST['shares']),
					price=float(request.POST['price']),
					commission=float(request.POST['commission']),)
			usr_tran_obj.save()
		except staticStockInfo.DoesNotExist:
			return HttpResponse("ticker")
		except:
			return HttpResponse("na")
		else:
			return HttpResponse("success")
	else:
		return HttpResponseRedirect(reverse('pfinance:login'))





