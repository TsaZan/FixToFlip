from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView

from FixToFlip.properties.models import Property


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard-index.html'
    login_url = 'index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['properties_count'] = Property.objects.filter(owner=self.request.user).count()
        context['properties_in_repair'] = Property.objects.filter(owner=self.request.user,
                                                                  property_condition='Under repair').count()
        context['user'] = self.request.user
        return context


class DashboardTasksView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/tasks.html'
    login_url = 'index'


