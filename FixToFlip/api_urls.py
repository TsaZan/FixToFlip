from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from FixToFlip.blog.views import BlogIndexView, CategoryView, BlogPostAPIView, PostsByCategoryAPIView
from FixToFlip.properties.views import PropertyListApiView, PropertyExpensesApiView, \
    PropertyApiView, BulkPropertyCreate

app_name = "FixToFlip API"

urlpatterns = [

    path('', include([
        # AUTHENTICATION API VIEWS
        path('token/', include([
            path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        ])),

        # PROPERTY MODEL API VIEWS
        path('properties/', include([
            path('', PropertyListApiView.as_view(), name='property_list_api'),
            path('bulk/', BulkPropertyCreate.as_view(), name='bulk_property_list_api'),
            path('<int:pk>/', PropertyApiView.as_view(), name='property_details_api'),
            path('<int:pk>/expenses/', PropertyExpensesApiView.as_view(), name='property_expenses_api')
        ])),

        # BLOG MODEL API VIEWS
        path('blog/', include([
            path('', BlogIndexView.as_view(), name='blog_api'),
            path('categories/', CategoryView.as_view(), name='category_api'),
            path('categories/<int:category_id>/', PostsByCategoryAPIView.as_view(), name='post_by_category'),
            path('<str:slug>/', BlogPostAPIView.as_view(), name='blog_post_api'),

        ]))
    ]))]
