from django import forms


class FlashcardForm(forms.Form):
    user_response = forms.CharField(max_length=100)