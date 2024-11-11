from django.urls import path, include

from FixToFlip.accounts.views import ProfileEditView, AccountDeleteView
from FixToFlip.common.views import AjaxLoginView, AjaxSignupView, CustomPasswordResetView

urlpatterns = [
    path('', include([
        path('login/', AjaxLoginView.as_view(), name='ajax_login'),
        path("signup/", AjaxSignupView.as_view(), name="ajax_signup"),
        path('password/reset/', CustomPasswordResetView.as_view(), name='account_reset_password'),

    ])),
    path('<int:pk>/', include([
        path('profile/', ProfileEditView.as_view(), name='profile_edit'),
        path('delete/', AccountDeleteView.as_view(), name='delete_account'),

    ])),
]