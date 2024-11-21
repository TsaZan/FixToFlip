from django.urls import path, include

from FixToFlip.blog.views import BlogMainPageView, BlogPostView, delete_comment

urlpatterns = [
    path('', BlogMainPageView.as_view(), name='blog_main_page'),
    path('<str:slug>/', BlogPostView.as_view(), name='blog_post_page'),
    path('comments/', include([
        path('', BlogPostView.as_view(), name='blog_comments'),
        path('<int:pk>/delete/', delete_comment, name='delete_comment'),
    ])),
]