from django import forms

class AddComputerForm(forms.Form):
    uid = forms.RegexField(regex="^[a-zA-Z][a-zA-Z\-_\d.]+$", error_message="UID entry must consist of alphanumeric characters")
