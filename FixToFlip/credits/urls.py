from django.urls import path, include

from FixToFlip.credits.views import (EditCreditView, DeleteCreditView,
                                     DashboardCreditsView, CreditDetailsView)

urlpatterns = [
    path('', DashboardCreditsView.as_view(), name='credits'),
    path('<int:pk>/', CreditDetailsView, name='credit_details'),
    path('<int:pk>/edit/', EditCreditView.as_view(), name='edit_credit'),
    path('<int:pk>/delete/', DeleteCreditView.as_view(), name='add_credit'),
]
