from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from djmoney.money import Money

from FixToFlip.credits.forms import CreditAddForm, CreditPaymentForm, CreditEditForm
from FixToFlip.credits.models import Credit, CreditPayment
from FixToFlip.money_operations import credit_reminder_calculation, credit_balance, interest_paid
from FixToFlip.properties.models import PropertyFinancialInformation


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
        context['header_title'] = 'Credits Dashboard'

        return context


class CreditAddView(LoginRequiredMixin, CreateView):
    model = Credit
    form_class = CreditAddForm
    template_name = 'dashboard/add-credit.html'
    success_url = reverse_lazy('dashboard_credits')

    def form_valid(self, form):
        form.instance.credit_owner = self.request.user
        return super().form_valid(form)


class CreditDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/credit-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        credit = Credit.objects.get(id=self.kwargs['pk'])
        properties = PropertyFinancialInformation.objects.all().filter(credit=credit)
        credit_payments = CreditPayment.objects.filter(credit_id=credit.id)
        total = credit_payments.aggregate(total_interest=Sum('interest_amount'),
                                          total_principal=Sum('principal_amount'))
        if total['total_interest'] is None:
            total['total_interest'] = 0
        if total['total_principal'] is None:
            total['total_principal'] = 0
        full_payment = total['total_interest'] + total['total_principal']
        if credit_payments.exists():
            currency = credit_payments.first().interest_amount.currency
        else:
            currency = 'EUR'

        total_interest = Money(total['total_interest'] or 0, currency)
        total_principal = Money(total['total_principal'] or 0, currency)
        full_payment = Money(full_payment, currency)

        form = CreditPaymentForm()
        context['credit'] = credit
        context['form'] = form
        context['credit_payments'] = credit_payments
        context['full_payment'] = full_payment

        context['total_interest'] = total_interest
        context['total_principal'] = total_principal
        context['properties'] = properties
        return context

    def post(self, request, *args, **kwargs):
        credit = Credit.objects.get(id=self.kwargs['pk'])
        form = CreditPaymentForm(request.POST or None, credit=credit)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.credit = credit
            payment.save()
            return redirect('credit_details', pk=credit.id)
        return render(request, 'dashboard/credit-details.html', {'credit': credit, 'form': form})


class EditCreditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Credit
    form_class = CreditEditForm
    template_name = 'dashboard/edit-credit.html'
    success_url = reverse_lazy('dashboard_credits')

    def test_func(self):
        credit = self.get_object()
        return self.request.user == credit.credit_owner

    def form_valid(self, form):
        form.instance.credit_owner = self.request.user
        return super().form_valid(form)


class DeleteCreditView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Credit
    template_name = 'dashboard/delete-credit.html'
    success_url = reverse_lazy('dashboard_credits')

    def test_func(self):
        credit = self.get_object()
        return self.request.user == credit.credit_owner
