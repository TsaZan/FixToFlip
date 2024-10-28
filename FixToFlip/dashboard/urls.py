from urllib import request

from django.shortcuts import render
from django.urls import path, include

from FixToFlip.dashboard.views import DashboardView, DashboardPropertyView, DashboardTasksView, PropertyAddView, \
    PropertyDetailsView, ProfileEditTemplate, DashboardExpensesView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('properties/', DashboardPropertyView.as_view(), name='dashboard_properties'),
    path('add-property/', PropertyAddView.as_view(), name='add_property'),
    path('tasks/', DashboardTasksView.as_view(), name='dashboard_tasks'),

    path('credits/', DashboardPropertyView.as_view(), name='dashboard_credits'),
    path('add-credit/', PropertyAddView.as_view(), name='add_credit'),
    path('expenses/', DashboardExpensesView.as_view(), name='dashboard_expenses'),

    path('<int:pk>/property/', PropertyDetailsView.as_view(), name='property_details'),
    path('profile/', ProfileEditTemplate.as_view(), name='profile_edit'),
    path('roi/', render, {'template_name': 'dashboard/ROI-calc.html'}, name='roi_calc')
]