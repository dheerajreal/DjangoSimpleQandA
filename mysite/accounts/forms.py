from django.contrib.auth.forms import UserCreationForm

from django import forms


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(
        help_text="Your email address is required for password reset in case you forget your password", required=True)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = (self.cleaned_data["email"])
        if commit:
            user.save()
        return user
