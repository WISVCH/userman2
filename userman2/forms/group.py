from django import forms
from userman2.model import user


class PossibleUsers:
    def __iter__(self):
        return iter([("", "")] + [(username, username) for username in user.GetAllUserNames()])


class GroupsForm(forms.Form):
    uid = forms.RegexField(regex="^[a-zA-Z\d \-\$]+$", required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Filter by member'}))
    cn = forms.RegexField(regex="^[^:^,]+$", required=False,
                          widget=forms.TextInput(attrs={'placeholder': 'Filter by name'}))


class AddUserForm(forms.Form):
    user = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.fields['user'].choices = PossibleUsers()


class AddGroupForm(forms.Form):
    common_name = forms.RegexField(regex="^[a-z\d\-_]+$", required=True)
