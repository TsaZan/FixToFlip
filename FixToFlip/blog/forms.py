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
                'class': 'form-control mb-20'
            }),
            'keywords': forms.TextInput(attrs={'required': 'required'}),
        }

        error_messages = {
            'title': {
                'unique': 'Title must be unique.'
            },
            'content': {
                'max_length': 'Content is too long.'
            },
            'category': {
                'required': 'Category is required.',
                'blank': 'Category is required.'
            }
        }


class BlogPostDeleteForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = []


class BlogEditForm(AddBlogPostForm):
    pass
