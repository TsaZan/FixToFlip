import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView
from rest_framework import generics
from django.views.generic import View

from FixToFlip.accounts.models import BaseAccount
from FixToFlip.blog.forms import BlogPostForm
from FixToFlip.blog.models import BlogPost, Category
from FixToFlip.blog.serializers import BlogPostSerializer, CategorySerializer


class BlogIndexView(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BlogPostAPIView(generics.ListAPIView):

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return BlogPost.objects.filter(slug=slug)

    serializer_class = BlogPostSerializer


def get_extra_context():
    return {

    }


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
            'form': BlogPostForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request, slug=None):
        form = BlogPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = BaseAccount.objects.get(username='Tsanko')  # TODO: get current user
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
