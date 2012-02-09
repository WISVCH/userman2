from django import forms

class AddComputerForm(forms.Form):
    uid = forms.RegexField(regex="^[a-z][a-z\-_\d.]+$", error_message="UID entry must consist of lowercase alphanumeric characters")
