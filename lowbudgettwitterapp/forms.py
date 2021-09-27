from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        min_length=4,
        max_length=15,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "minlength": "4",
                "maxlength": "15",
                "id": "floatingInput",
            }
        ),
    )
    email = forms.EmailField(
        max_length=150,
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "id": "floatingInput"}),
    )
    password1 = forms.CharField(
        required=True,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "id": "floatingPassword", "minlength": "8"}
        ),
    )
    password2 = forms.CharField(
        required=True,
        min_length=8,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "id": "floatingPassword", "minlength": "8"}
        ),
    )

    class Meta:
        model = Account
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "minlength": "4", "id": "floatingInput"}
        ),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "id": "floatingPassword"}
        ),
    )



class ProfileForm(forms.Form):
    display_name = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "minlength": "4",
                "maxlength": "20",
                "id": "floatingdisplayname",
            }
        ),
    )
    bio = forms.CharField(
        max_length=100,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "maxlength": "100",
                "id": "floatingbio",
                "rows": "150",
            }
        ),
    )
    profile_pic = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                "id":"profile-pic-upload"
            }
        )
    )


"""
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["user", "display_name", "profile_pic", "bio"]
        widgets = {
            "display_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "minlength": "4",
                    "maxlength": "20",
                    "id": "floatingdisplayname",
                }
            ),
            #"profile_pic": forms.FileInput(),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "maxlength": "100",
                    "id": "floatingbio",
                    "rows": 150,
                }
            ),
        }
"""