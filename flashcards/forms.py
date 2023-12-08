from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class FlashcardForm(forms.Form):
    user_response = forms.CharField(
        max_length=10, label="", widget=forms.TextInput(attrs={"class": "form-control"})
    )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254, widget=forms.TextInput(attrs={"autofocus": True})
    )
    password = forms.CharField(widget=forms.PasswordInput)


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=254, widget=forms.TextInput(attrs={"autofocus": True})
    )
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
