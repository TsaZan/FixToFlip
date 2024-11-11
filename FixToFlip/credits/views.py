from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from FixToFlip.credits.forms import CreditAddForm, CreditPaymentForm
from FixToFlip.credits.models import Credit, CreditPayment
from FixToFlip.money_operations import credit_reminder_calculation, credit_balance, interest_paid


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
            credit.balance = credit_balance(credit.id)
            if CreditPayment.objects.filter(credit_id=credit.id):
                credit.interest_paid = interest_paid(credit.id)
                credit.last_payment = CreditPayment.objects.filter(credit_id=credit.id).first().payment_date
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


class EditCreditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        property = self.get_object()
        return self.request.user == property.owner


class DeleteCreditView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    def test_func(self):
        property = self.get_object()
        return self.request.user == property.owner

