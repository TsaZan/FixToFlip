from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from rest_framework import generics
from django.views.generic import View
from rest_framework.permissions import AllowAny

from FixToFlip.blog.filters import BlogPostsFilter
from FixToFlip.blog.forms import BlogCommentForm, AddBlogPostForm, BlogPostDeleteForm
from FixToFlip.blog.models import BlogPost, Category, Comment
from FixToFlip.blog.serializers import BlogPostSerializer, CategorySerializer


class BlogMainPageView(TemplateView):
    model = BlogPost
    template_name = "blog/blog.html"

    def get(self, *args, **kwargs):

        if "q" in self.request.GET:
            q = self.request.GET.get("q", "")
            posts = BlogPost.objects.filter(content__icontains=q)

        elif "category" in self.request.GET:
            category = self.request.GET.get("category", "")
            posts = BlogPost.objects.filter(category__name=category)

        else:
            posts = BlogPost.objects.all()

        blog_posts_list = posts
        paginator = Paginator(blog_posts_list, 6)
        page_number = self.request.GET.get("page")
        posts = paginator.get_page(page_number)

        context = {
            "posts": posts,
            "categories": Category.objects.all(),
        }

        return render(self.request, self.template_name, context)


class BlogPostView(View):
    template_name = "blog/blog-post.html"

    def get(self, request, slug=None):
        post = get_object_or_404(BlogPost, slug=slug) if slug else None

        context = {
            "post": post,
            "posts": BlogPost.objects.all()[:5],
            "categories": Category.objects.all(),
            "keywords": post.keywords.split(",") if post else [],
            "form": BlogCommentForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request, slug=None):
        form = BlogCommentForm(request.POST)
        post = get_object_or_404(BlogPost, slug=slug) if slug else None
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            if slug:
                new_post.post = get_object_or_404(BlogPost, slug=slug)
            new_post.save()
            return redirect("blog_post_page", slug=slug)

        context = {
            "post": post,
            "form": form,
            "posts": BlogPost.objects.all()[:5],
            "categories": Category.objects.all(),
        }
        return render(request, self.template_name, context)


class DashboardBlogPostsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    model = BlogPost
    template_name = "blog/blogposts-list.html"
    filterset_class = BlogPostsFilter
    login_url = "index"

    def test_func(self):
        return self.request.user.groups.filter(name__icontains="moderator").exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_posts = BlogPost.objects.all()
        blog_posts = blog_posts.annotate(comments_count=Count("comments"))
        blog_post_filter = BlogPostsFilter(self.request.GET, queryset=blog_posts)
        sorted_posts = blog_post_filter.qs.distinct()
        paginator = Paginator(sorted_posts, 5)
        page_number = self.request.GET.get("page")
        posts = paginator.get_page(page_number)
        if "q" in self.request.GET:
            q = self.request.GET.get("q", "")
            posts = BlogPost.objects.filter(title__icontains=q)

        context["posts"] = posts
        context["filter"] = blog_post_filter
        context["header_title"] = "Blog Dashboard"
        context["search_placeholder"] = "Search post by title..."
        return context


class AddBlogPostView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = BlogPost
    form_class = AddBlogPostForm
    template_name = "blog/add-blogpost.html"
    success_url = reverse_lazy("dashboard_blogposts")
    login_url = "index"

    def test_func(self):
        return self.request.user.groups.filter(name__icontains="moderator").exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_title"] = "Add Blog Post"
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditBlogPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    permission_required = "blog.edit_blogpost"
    permission_denied_message = "You do not have permission to edit this post"

    def test_func(self):
        return self.request.user.groups.filter(name__icontains="moderator").exists()

    model = BlogPost
    form_class = AddBlogPostForm
    template_name = "blog/edit-blogpost.html"

    def get_object(self, queryset=None):
        return BlogPost.objects.get(slug=self.kwargs["slug"])

    def get_success_url(self):
        slug = self.object.slug
        return reverse_lazy("edit_blogpost", kwargs={"slug": slug})


class DeleteBlogPostView(
    PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    model = BlogPost
    form_class = BlogPostDeleteForm
    template_name = "blog/delete-blogpost.html"
    success_url = reverse_lazy("dashboard_blogposts")
    permission_required = "blog.delete_blogpost"
    permission_denied_message = "You do not have permission to delete this post"
    login_url = "index"

    def test_func(self):
        return self.request.user.groups.filter(name="super_moderator").exists()

    def get_object(self, queryset=None):
        return BlogPost.objects.get(slug=self.kwargs["slug"])

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class BlogCommentsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    model = Comment
    template_name = "blog/comments-list.html"
    login_url = "index"

    def test_func(self):
        return self.request.user.groups.filter(name__icontains="moderator").exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.all()

        if "q" in self.request.GET:
            q = self.request.GET.get("q", "")
            comments = Comment.objects.filter(
                Q(content__icontains=q) | Q(post__title__icontains=q)
            )

        paginator = Paginator(comments, 5)
        page_number = self.request.GET.get("page")
        comments = paginator.get_page(page_number)

        context["comments"] = comments
        context["header_title"] = "Comments Dashboard"
        context["search_placeholder"] = "Search by content or post title..."
        return context


@user_passes_test(lambda user: user.groups.filter(name__icontains="moderator").exists())
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect("blog_comments")


""" API Views """


class BlogIndexView(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class PostsByCategoryAPIView(generics.ListAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        return BlogPost.objects.filter(category_id=category_id)


class BlogPostAPIView(generics.ListAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return BlogPost.objects.filter(slug=slug)
