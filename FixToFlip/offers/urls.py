from django.urls import path, include

from FixToFlip.offers.views import offers_main_page, add_offer, edit_offer, delete_offer, details_offer
urlpatterns = [
    path('', offers_main_page, name='offers_main_page'),
    path('<int:pk>/', details_offer, name='detail_offer'),
    path('add/', add_offer, name='add_offer'),
    path('<int:pk>/edit/', edit_offer, name='edit_offer'),
    path('<int:pk>/delete/', delete_offer, name='delete_offer'),
]