from django import forms
from FixToFlip.accounts.models import Profile, BaseAccount


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']

        widgets = {
            'url': forms.TextInput(attrs={'placeholder': 'http://....'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'Company Name'}),

        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = BaseAccount
        exclude = ['is_staff', 'is_superuser', 'is_active', 'user_permissions', 'date_joined', 'username', 'groups',
                   'password']

        widgets = {
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),

        }


class UserDeleteForm(UserEditForm):
    pass
