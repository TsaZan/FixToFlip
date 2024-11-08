from django.urls import path, include
from FixToFlip.common.views import index, about_us, contact, faq, \
    CustomPasswordResetView, AjaxLoginView, AjaxSignupView

urlpatterns = [
    path('', index, name='index'),
    path('about-us/', about_us, name='about-us'),
    path('contact/', contact, name='contact'),
    path('faq/', faq, name='faq'),
    path('accounts/', include('allauth.urls'), name='accounts_main_page'),
    # path('accounts/ajax-login/', ajax_login_view, name='ajax_login'),
    # path('accounts/ajax-signup/', ajax_signup_view, name='ajax_signup'),
    path('ajax/login/', AjaxLoginView.as_view(), name='ajax_login'),
    path("ajax/signup/", AjaxSignupView.as_view(), name="ajax_signup"),
    path('accounts/password/reset/', CustomPasswordResetView.as_view(), name='account_reset_password'),
]
