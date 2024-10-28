from django.urls import path, include

from FixToFlip.blog.views import BlogMainPageView, BlogPostView

urlpatterns = [
    path('', BlogMainPageView.as_view(), name='blog_main_page'),
    path('<str:slug>/', BlogPostView.as_view(), name='blog_post_page'),
]