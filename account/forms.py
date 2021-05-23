from django import forms
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


class LoginForm(forms.Form):
    """Create a login form for users."""
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """Create a user registration form."""
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Repeat Password",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "email")

    def clean_password2(self):
        """Prepare password data."""
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match.")

        return cd["password2"]


class UserEditForm(forms.ModelForm):
    """Enable users to edit their personal data."""
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class ProfileEditForm(forms.ModelForm):
    """Users can enable their profile data."""
    class Meta:
        model = Profile
        fields = ("date_of_birth", "photo")
