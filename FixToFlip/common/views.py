from allauth.account.forms import LoginForm
from allauth.account.views import LoginView, login

from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    return render(request, 'common/index.html')


def about_us(request):
    return render(request, 'common/about-us.html')


def contact(request):
    return render(request, 'common/contact.html')


def faq(request):
    return render(request, 'common/faq.html')


# def login(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST or None)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 auth_login(request, user)
#                 return redirect('/')
#         else:
#             return render(request, 'common/login_modal.html', {"loginctx": form})
#     return render(request, 'common/login_modal.html')


def ajax_login_view(request):
    if request.method == "POST":
        request.session['show_loader'] = True
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            request.session['show_loader'] = False
            login(request, form.user)
            return JsonResponse({"success": True})
        else:
            request.session['show_loader'] = False

            # Връщаме съобщенията за грешки в текстов формат
            errors = {field: [error["message"] for error in errors] for field, errors in form.errors.get_json_data().items()}
            return JsonResponse({"success": False, "errors": errors})
    return JsonResponse({"success": False, "errors": "Invalid request"})
