from django.urls import path
from FixToFlip.dashboard.views import DashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
]
