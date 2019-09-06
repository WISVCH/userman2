from django import forms


class AddComputerForm(forms.Form):
    uid = forms.RegexField(
        regex="^[a-z][a-z\-_\d.]+$",
        error_messages={"invalid": "UID entry must consist of lowercase alphanumeric characters"},
    )
