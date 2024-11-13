from django.urls import path, include

from FixToFlip.properties.views import add_expense

urlpatterns = [
    path('', include([
        path('<int:pk>/expense/', add_expense, name='add_expense'),
    ])),
]