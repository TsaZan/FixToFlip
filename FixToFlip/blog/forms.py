from django import forms

from FixToFlip.blog.models import Comment, BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category']

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']








