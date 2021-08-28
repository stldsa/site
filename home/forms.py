from django import forms


class EmailSubmissionForm(forms.Form):
    email = forms.EmailField()