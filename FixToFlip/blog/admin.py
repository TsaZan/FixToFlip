from django.contrib import admin
from FixToFlip.blog.models import BlogPost, Category, Comment

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'author',
        'category',
        'comment_count',
    )
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'content',
        'created_at',
    )
