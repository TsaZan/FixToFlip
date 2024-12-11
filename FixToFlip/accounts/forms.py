from django import forms
from FixToFlip.accounts.models import Profile, BaseAccount


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "profile_type",
            "phone_number",
            "preferred_currency",
            "user_location",
            "profile_picture",
            "company_name",
            "company_phone",
            "company_location",
            "company_url",
            "company_name",
        ]

        widgets = {
            "company_url": forms.TextInput(attrs={"placeholder": "http://...."}),
            "company_name": forms.TextInput(attrs={"placeholder": "Company Name"}),
            "profile_picture": forms.ClearableFileInput(
                attrs={
                    "type": "file",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={"placeholder": "eg. +359 000 000 000"}
            ),
            "company_phone": forms.TextInput(
                attrs={"placeholder": "eg. +359 000 000 000"}
            ),
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = BaseAccount
        exclude = [
            "is_staff",
            "is_superuser",
            "is_active",
            "user_permissions",
            "date_joined",
            "username",
            "groups",
            "password",
        ]

        widgets = {
            "email": forms.TextInput(attrs={"readonly": "readonly"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
        }


class UserDeleteForm(UserEditForm):
    pass
