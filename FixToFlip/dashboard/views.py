from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from FixToFlip.accounts.models import BaseAccount
from FixToFlip.properties.forms import PropertyAddForm
from FixToFlip.properties.models import Property


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard-index.html'
    if login_required:
        login_url = 'index'


class DashboardTasksView(LoginRequiredMixin, TemplateView):
    if login_required:
        login_url = 'index'

    template_name = 'dashboard/tasks.html'


class ProfileEditTemplate(LoginRequiredMixin, TemplateView):
    if login_required:
        login_url = 'index'

    model = BaseAccount
    template_name = 'dashboard/profile.html'
    success_url = reverse_lazy('dashboard')
    fields = '__all__'


class DashboardCreditsView(LoginRequiredMixin, TemplateView):
    if login_required:
        login_url = 'index'

    template_name = 'dashboard/credits-list.html'


class DashboardExpensesView(LoginRequiredMixin, TemplateView):
    if login_required:
        login_url = 'index'

    template_name = 'dashboard/expenses-list.html'


class CreditAddView(LoginRequiredMixin, CreateView):
    if login_required:
        login_url = 'index'

    model = Property
    form_class = PropertyAddForm
    template_name = 'dashboard/add-credit.html'
    success_url = reverse_lazy('credits_main_page')



