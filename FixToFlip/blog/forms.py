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


class AddBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category', 'image', 'keywords']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': ' form-control mb-20',
                'type': 'file',
                'accept': 'image/*',
                'id': 'customFile'
            }),
            'category': forms.Select(attrs={
                'class': 'dash-input-wrapper mb-20 nice-select'
            }),
        }


class BlogPostDeleteForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = []


class BlogEditForm(AddBlogPostForm):
    pass
