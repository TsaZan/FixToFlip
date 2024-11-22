from django.urls import path
from FixToFlip.common.views import index, about_us, contact, faq

urlpatterns = [
    path('', index, name='index'),
    path('about-us/', about_us, name='about-us'),
    path('contact/', contact, name='contact'),
    path('faq/', faq, name='faq'),

]
