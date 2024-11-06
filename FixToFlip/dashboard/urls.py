from urllib import request

from django.shortcuts import render
from django.urls import path, include

from FixToFlip.blog.views import BlogPostsView, EditBlogPostView, AddBlogPostView, DeleteBlogPostView
from FixToFlip.dashboard.views import DashboardView, DashboardTasksView, \
    ProfileEditTemplate, DashboardExpensesView, DashboardCreditsView, CreditAddView
from FixToFlip.properties.views import DashboardPropertiesView, PropertyDetailsView, property_add_view

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    path('properties/', include([
        path('', DashboardPropertiesView.as_view(), name='dashboard_properties'),
        path('add-property/', property_add_view, name='add_property'),
        path('<int:pk>/view/', PropertyDetailsView.as_view(), name='property_details'),
    ])),

    path('tasks/', DashboardTasksView.as_view(), name='dashboard_tasks'),

    path('credits/', include([
        path('', DashboardCreditsView.as_view(), name='dashboard_credits'),
        path('add-credit/', CreditAddView.as_view(), name='add_credit'),
    ])),

    path('expenses/', DashboardExpensesView.as_view(), name='dashboard_expenses'),

    path('profile/', ProfileEditTemplate.as_view(), name='profile_edit'),

    path('blogposts/', include([
        path('', BlogPostsView.as_view(), name='dashboard_blogposts'),
        path('<str:slug>/edit/', EditBlogPostView.as_view(), name='edit_blogpost'),
        path('add/', AddBlogPostView.as_view(), name='add_blogpost'),
        path('<str:slug>/delete/', DeleteBlogPostView.as_view(), name='delete_blogpost'),
    ]))
]
