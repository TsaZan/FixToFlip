from django import forms

from FixToFlip.blog.models import Comment


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']








