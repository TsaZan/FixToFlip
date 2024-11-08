from django.urls import path, include

from FixToFlip.credits.views import (EditCreditView, DeleteCreditView, CreditPaymentView,
                                     DashboardCreditsView, CreditDetailsView)

urlpatterns = [
    path('', DashboardCreditsView.as_view(), name='credits'),
    path('<int:pk>/', CreditDetailsView, name='credit_details'),
    path('<int:pk>/edit/', EditCreditView, name='edit_credit'),
    path('<int:pk>/delete/', DeleteCreditView, name='add_credit'),
    path('<int:pk>/payment/', CreditPaymentView, name='delete_credit'),
]
