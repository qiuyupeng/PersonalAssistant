from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


from .models import userInfo, userTransaction
from .usermodels import portfolio


def test(request):
	return HttpResponse("how are you")