from django.urls import path, include
from FixToFlip.common.views import index, about_us, contact, faq, ajax_login_view

urlpatterns = [
    path('', index, name='index'),
    path('about-us/', about_us, name='about-us'),
    path('contact/', contact, name='contact'),
    path('faq/', faq, name='faq'),
    path('accounts/ajax-login/', ajax_login_view, name='ajax_login'),

]
