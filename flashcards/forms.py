from django import forms


class FlashcardForm(forms.Form):
    user_response = forms.CharField(
        max_length=10, label="", widget=forms.TextInput(attrs={"class": "form-control"})
    )
