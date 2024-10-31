from cloudinary.forms import CloudinaryJsFileField
from django import forms

from FixToFlip.blog.models import BlogPost
from FixToFlip.properties.models import Property


class PropertyAddForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'


class AddBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category', 'image', 'keywords']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'dash-input-wrapper mb-20 attached-file d-flex align-items-center justify-content-between mb-15'
            }),
        }


class BlogPostDeleteForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = []


class BlogEditForm(AddBlogPostForm):
    pass
