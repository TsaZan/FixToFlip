from allauth.account.views import login, LoginView, SignupView, PasswordResetView
from django.http import JsonResponse
from django.shortcuts import render

from FixToFlip.accounts.models import Profile


# Create your views here.
def index(request):
    return render(request, 'common/index.html')


def about_us(request):
    return render(request, 'common/about-us.html')


def contact(request):
    return render(request, 'common/contact.html')


def faq(request):
    return render(request, 'common/faq.html')


class AjaxLoginView(LoginView):
    def form_valid(self, form):
        login(self.request, form.user)
        return JsonResponse({'success': True, 'location': '#'})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})


class AjaxSignupView(SignupView):

    def form_valid(self, form):
        super().form_valid(form)
        login(self.request, self.user)
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors.as_json()})


class CustomPasswordResetView(PasswordResetView):
    template_name = 'common/login_modal.html'
