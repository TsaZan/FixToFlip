from allauth.account.forms import SignupForm
from django.contrib.auth import login

from django.contrib.auth import authenticate

from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'common/index.html')


def about_us(request):
    return render(request, 'common/about-us.html')


def contact(request):
    return render(request, 'common/contact.html')


def faq(request):
    return render(request, 'common/faq.html')


