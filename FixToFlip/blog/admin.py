from django.contrib import admin
from unfold.admin import ModelAdmin
from FixToFlip.blog.models import BlogPost, Category, Comment


@admin.register(BlogPost)
class BlogPostAdmin(ModelAdmin):
    list_display = (
        'title',
        'keywords',
        'author',
        'category',
        'comment_count',
    )
    search_fields = ('title',
                     'keywords',
                     )
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'author', 'category', 'keywords', 'image')
        }),
        ('Content', {
            'fields': ('content',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = (
        'name',
        'post_count',
    )


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = (
        'author',
        'content',
        'created_at',
    )
