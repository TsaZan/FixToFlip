from django.urls import path, include
from FixToFlip.dashboard.views import DashboardView, DashboardTasksView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    path('tasks/', DashboardTasksView.as_view(), name='dashboard_tasks'),

]
