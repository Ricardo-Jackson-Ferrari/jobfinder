from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=100, required=True)
    subject = forms.CharField(max_length=50, required=True)
    message = forms.CharField(max_length=500, widget=forms.Textarea)
