from django.urls import path, include

from FixToFlip.blog.views import (
    BlogMainPageView,
    BlogPostView,
    delete_comment,
    DashboardBlogPostsView,
    EditBlogPostView,
    AddBlogPostView,
    DeleteBlogPostView,
    BlogCommentsView,
)

urlpatterns = [
    path(
        "moderate/",
        include(
            [
                path("", DashboardBlogPostsView.as_view(), name="dashboard_blogposts"),
                path(
                    "<str:slug>/edit/", EditBlogPostView.as_view(), name="edit_blogpost"
                ),
                path("add/", AddBlogPostView.as_view(), name="add_blogpost"),
                path(
                    "<str:slug>/delete/",
                    DeleteBlogPostView.as_view(),
                    name="delete_blogpost",
                ),
                path(
                    "comments/",
                    include(
                        [
                            path("", BlogCommentsView.as_view(), name="blog_comments"),
                        ]
                    ),
                ),
                path(
                    "comments/",
                    include(
                        [
                            path("", BlogPostView.as_view(), name="blog_comments"),
                            path(
                                "<int:pk>/delete/",
                                delete_comment,
                                name="delete_comment",
                            ),
                        ]
                    ),
                ),
            ]
        ),
    ),
    path("", BlogMainPageView.as_view(), name="blog_main_page"),
    path("<str:slug>/", BlogPostView.as_view(), name="blog_post_page"),
]
