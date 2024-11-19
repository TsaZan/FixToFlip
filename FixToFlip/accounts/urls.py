from django.urls import path, include

from FixToFlip.accounts.views import ProfileEditView, AccountDeleteView, ajax_login, ajax_signup

urlpatterns = [
    path('', include([
        path('login/', ajax_login, name='ajax_login'),
        path("signup/", ajax_signup, name="ajax_signup"),

    ])),
    path('<int:pk>/', include([
        path('profile/', ProfileEditView.as_view(), name='profile_edit'),
        path('delete/', AccountDeleteView.as_view(), name='delete_account'),

    ])),
]