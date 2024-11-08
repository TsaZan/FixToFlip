from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from FixToFlip.credits.forms import CreditAddForm
from FixToFlip.credits.models import Credit
from FixToFlip.money_operations import credit_reminder_calculation


class DashboardCreditsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/credits-list.html'
    login_url = 'index'

    def get_context_data(self, **kwargs):
        credits_list = Credit.objects.filter(credit_owner=self.request.user)
        paginator = Paginator(credits_list, 5)
        page_number = self.request.GET.get('page')
        credits = paginator.get_page(page_number)
        for credit in credits:
            credit.remainder = credit_reminder_calculation(credit.id)
        context = super().get_context_data(**kwargs)
        context['credits'] = credits

        return context


def CreditDetailsView(request, pk):
    pass


class CreditAddView(LoginRequiredMixin, CreateView):
    model = Credit
    form_class = CreditAddForm
    template_name = 'dashboard/add-credit.html'
    success_url = reverse_lazy('credits')

    def form_valid(self, form):
        form.instance.credit_owner = self.request.user
        return super().form_valid(form)




def EditCreditView(request, pk):
    pass


def DeleteCreditView(request, pk):
    pass


def CreditPaymentView(request, pk):
    pass
