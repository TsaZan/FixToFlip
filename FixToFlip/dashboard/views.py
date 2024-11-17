from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView

from FixToFlip.properties.models import Property


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard-index.html'
    login_url = 'index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_properties'] = Property.objects.filter(owner=self.request.user)
        context['properties_in_repair'] = Property.objects.filter(
            owner=self.request.user, property_condition='Under repair')

        context['properties_for_sale'] = Property.objects.filter(
            owner=self.request.user, property_condition='For sale')

        context['properties_sold'] = Property.objects.filter(
            owner=self.request.user, property_condition='Sold')
        context['user'] = self.request.user
        context['header_title'] = 'Dashboard'
        return context


class DashboardTasksView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/tasks.html'
    login_url = 'index'


