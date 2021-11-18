from django import forms


class SearchForm(forms.Form):
    title = forms.CharField(required=False)
    author = forms.CharField(required=False)
    ISBN_number = forms.CharField(label="ISBN number", required=False)
