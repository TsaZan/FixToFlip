from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from FixToFlip.blog.views import BlogIndexView, CategoryView, BlogPostAPIView, PostsByCategoryAPIView
from FixToFlip.offers.views import AllOffersAPIView, OfferAPIView
from FixToFlip.properties.views import PropertyListApiView, PropertyExpensesApiView, \
    PropertyApiView, BulkPropertyCreate, PropertyExpenseNoteCreateAPIView

app_name = "FixToFlip API"

urlpatterns = [

    path('', include([
        # AUTHENTICATION API VIEWS
        path('token/', include([
            path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        ])),

        path('properties/', include([
            path('', PropertyListApiView.as_view(), name='property_list_api'),
            path('bulk/', BulkPropertyCreate.as_view(), name='bulk_property_list_api'),
            path('<int:pk>/', PropertyApiView.as_view(), name='property_details_api'),
            path('<int:pk>/expenses/', PropertyExpensesApiView.as_view(), name='property_expenses_api'),
            path('<int:pk>/expenses/add/', PropertyExpenseNoteCreateAPIView.as_view(), name='create_expense'),
        ])),

        path('blog/', include([
            path('', BlogIndexView.as_view(), name='blog_api'),
            path('categories/', CategoryView.as_view(), name='category_api'),
            path('categories/<int:category_id>/', PostsByCategoryAPIView.as_view(), name='post_by_category'),
            path('<str:slug>/', BlogPostAPIView.as_view(), name='blog_post_api'),

        ])),

        path('offers/', include([
            path('', AllOffersAPIView.as_view(), name='api_offers'),
            path('<int:pk>/', OfferAPIView.as_view(), name='detail_offer'),

        ]))
    ])),

]
