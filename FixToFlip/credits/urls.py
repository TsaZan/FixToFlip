from django.urls import path, include

from FixToFlip.credits.views import (
    EditCreditView,
    DeleteCreditView,
    DashboardCreditsView,
    CreditDetailsView,
    CreditAddView,
    CreditPaymentDeleteView,
)

urlpatterns = [
    path(
        "",
        include(
            [
                path("", DashboardCreditsView.as_view(), name="dashboard_credits"),
                path("add-credit/", CreditAddView.as_view(), name="add_credit"),
            ]
        ),
    ),
    path(
        "<int:pk>/",
        include(
            [
                path("", CreditDetailsView.as_view(), name="credit_details"),
                path("edit/", EditCreditView.as_view(), name="edit_credit"),
                path("delete/", DeleteCreditView.as_view(), name="delete_credit"),
                path(
                    "delete-payment/",
                    CreditPaymentDeleteView.as_view(),
                    name="delete_credit_payment",
                ),
            ]
        ),
    ),
]
