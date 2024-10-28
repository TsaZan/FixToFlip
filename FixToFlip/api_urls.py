from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from FixToFlip.blog.views import BlogIndexView, CategoryView, BlogPostAPIView
from FixToFlip.properties.views import PropertyListView, PropertyDetailsView, PropertyExpensesView

app_name = "FixToFlip"

urlpatterns = [
    path('', include([
        # AUTHENTICATION API VIEWS
        path('token/', include([
            path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        ])),

        # PROPERTY MODEL API VIEWS
        path('properties/', include([
            path('', PropertyListView.as_view(), name='property_list_api'),
            path('properties/<int:pk>/', PropertyDetailsView.as_view(), name='property_details_api'),
            path('properties/<int:pk>/expenses/', PropertyExpensesView.as_view(), name='property_expenses_api')
        ])),

        # BLOG MODEL API VIEWS
        path('blog/', include([
            path('category/', CategoryView.as_view(), name='category_api'),
            path('', BlogIndexView.as_view(), name='blog_api'),
            path('<str:slug>/', BlogPostAPIView.as_view(), name='blog_post_api'),
        ]))
    ]))]
