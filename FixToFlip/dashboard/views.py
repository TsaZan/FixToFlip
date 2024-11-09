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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties_count'] = Property.objects.filter(owner=self.request.user).count()
        context['properties_in_repair'] = Property.objects.filter(owner=self.request.user,
                                                                  property_condition='Under repair').count()
        context['user'] = self.request.user
        return context


class DashboardTasksView(LoginRequiredMixin, TemplateView):
    if login_required:
        login_url = 'index'

    template_name = 'dashboard/tasks.html'
