from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from rest_framework import generics
from django.views.generic import View
from rest_framework.permissions import AllowAny

from FixToFlip.blog.forms import BlogCommentForm, AddBlogPostForm, BlogPostDeleteForm
from FixToFlip.blog.models import BlogPost, Category
from FixToFlip.blog.serializers import BlogPostSerializer, CategorySerializer


class BlogMainPageView(TemplateView):
    model = BlogPost
    template_name = 'blog/blog.html'

    def get(self, *args, **kwargs):
        context = {
            'posts': BlogPost.objects.all(),
            'categories': Category.objects.all(), }

        return render(self.request, self.template_name, context)


class BlogPostView(View):
    template_name = 'blog/blog-post.html'

    def get(self, request, slug=None):
        post = get_object_or_404(BlogPost, slug=slug) if slug else None

        context = {
            'post': post,
            'posts': BlogPost.objects.all()[:5],
            'categories': Category.objects.all(),
            'keywords': post.keywords.split(',') if post else [],
            'form': BlogCommentForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request, slug=None):
        form = BlogCommentForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            if slug:
                new_post.post = get_object_or_404(BlogPost, slug=slug)
            new_post.save()
            return redirect('blog_post_page', slug=slug)

        context = {
            'form': form,
            'posts': BlogPost.objects.all()[:5],
            'categories': Category.objects.all(),
        }
        return render(request, self.template_name, context)


class BlogPostsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    model = BlogPost
    template_name = 'dashboard/blogposts-list.html'
    login_url = 'index'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_posts = BlogPost.objects.all()
        paginator = Paginator(blog_posts, 5)
        page_number = self.request.GET.get('page')
        posts = paginator.get_page(page_number)
        context['posts'] = posts
        context['header_title'] = 'Blog Dashboard'
        return context


class AddBlogPostView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = BlogPost
    form_class = AddBlogPostForm
    template_name = 'dashboard/add-blogpost.html'
    success_url = reverse_lazy('dashboard_blogposts')
    login_url = 'index'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff


class EditBlogPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    if login_required:
        login_url = 'index'

    model = BlogPost
    form_class = AddBlogPostForm
    template_name = 'dashboard/edit-blogpost.html'

    def get_object(self, queryset=None):
        return BlogPost.objects.get(slug=self.kwargs['slug'])

    def get_success_url(self):
        slug = self.object.slug
        return reverse_lazy('edit_blogpost', kwargs={'slug': slug})

    def test_func(self):
        return self.request.user.is_staff


class DeleteBlogPostView(PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    form_class = BlogPostDeleteForm
    template_name = 'dashboard/delete-blogpost.html'
    success_url = reverse_lazy('dashboard_blogposts')
    permission_required = ('dashboard.delete_blogpost',)
    login_url = 'index'

    def get_object(self, queryset=None):
        return BlogPost.objects.get(slug=self.kwargs['slug'])

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staff


''' API Views '''


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
        category_id = self.kwargs['category_id']
        return BlogPost.objects.filter(category_id=category_id)


class BlogPostAPIView(generics.ListAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return BlogPost.objects.filter(slug=slug)
