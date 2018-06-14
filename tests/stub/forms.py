from django import forms


class TestForm(forms.Form):
    item = forms.CharField(max_length=30)
