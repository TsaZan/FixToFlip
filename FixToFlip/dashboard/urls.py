from django.urls import path, include
from FixToFlip.accounts.views import ProfileEditView, AccountDeleteView
from FixToFlip.blog.views import BlogPostsView, EditBlogPostView, AddBlogPostView, DeleteBlogPostView
from FixToFlip.credits.views import DashboardCreditsView, CreditAddView
from FixToFlip.dashboard.views import DashboardView, DashboardTasksView
from FixToFlip.properties.views import DashboardPropertiesView, PropertyDetailsView, property_add_view, \
    DashboardExpensesView, PropertyEditView, PropertyDeleteView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    path('properties/', include([
        path('', DashboardPropertiesView.as_view(), name='dashboard_properties'),
        path('add-property/', property_add_view, name='add_property'),
        path('<int:pk>/view/', PropertyDetailsView.as_view(), name='property_details'),
        path('<int:pk>/edit/', PropertyEditView.as_view(), name='edit_property'),
        path('<int:pk>/delete/', PropertyDeleteView.as_view(), name='delete_property'),
    ])),

    path('tasks/', DashboardTasksView.as_view(), name='dashboard_tasks'),

    path('credits/', include([
        path('', DashboardCreditsView.as_view(), name='dashboard_credits'),
        path('add-credit/', CreditAddView.as_view(), name='add_credit'),
    ])),

    path('expenses/', DashboardExpensesView.as_view(), name='dashboard_expenses'),

    # path('<int:pk>/', include([
    #     path('profile/', ProfileEditView.as_view(), name='profile_edit'),
    #     path('delete/', AccountDeleteView.as_view(), name='delete_account'),
    #
    # ]
    #
    # )),

    path('blogposts/', include([
        path('', BlogPostsView.as_view(), name='dashboard_blogposts'),
        path('<str:slug>/edit/', EditBlogPostView.as_view(), name='edit_blogpost'),
        path('add/', AddBlogPostView.as_view(), name='add_blogpost'),
        path('<str:slug>/delete/', DeleteBlogPostView.as_view(), name='delete_blogpost'),
    ]))
]
