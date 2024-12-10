from django.urls import path, include

from FixToFlip.offers.views import (
    EditOfferView,
    DashboardOffersView,
    add_offer_view,
    OfferDeleteView,
)

urlpatterns = [
    path("", DashboardOffersView.as_view(), name="offers_main_page"),
    path("add/<int:pk>/", add_offer_view, name="create_offer"),
    path(
        "<int:pk>/",
        include(
            [
                path("edit/", EditOfferView.as_view(), name="edit_offer"),
                path("delete/", OfferDeleteView.as_view(), name="delete_offer"),
            ]
        ),
    ),
]
