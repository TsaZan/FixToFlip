from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from FixToFlip.blog.models import Comment, BlogPost


class AddBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category', 'image', 'keywords']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': ' form-control mb-20',
                'type': 'file',
                'accept': 'image/*',
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


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    captcha = ReCaptchaField(widget=ReCaptchaV3())
