from django import forms
from userman2.model import user, alias

# The code under AddUserForm is only evaluated once at start-up, so if
# we create the list of choices there it will never be changed even if
# we add/remove items. The iterables below will be evaluated everytime
# the form is displayed.


class PossibleUsers:
    def __iter__(self):
        return iter([("", "")] + [(username, username) for username in user.GetAllUserNames()])


class PossibleAliases:
    def __iter__(self):
        return iter([("", "")] + [(username, username) for username in alias.getAllAliasNames()])


class AliasForm(forms.Form):
    uid = forms.RegexField(regex="^[a-zA-Z\d \-\$]+$", required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Filter by member'}))
    cn = forms.RegexField(regex="^[^:^,]+$", required=False,
                          widget=forms.TextInput(attrs={'placeholder': 'Filter by name'}))


class AddUserForm(forms.Form):
    uid = forms.ChoiceField(choices=[], required=False)
    alias = forms.ChoiceField(choices=[], required=False)
    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        super(AddUserForm, self).__init__(*args, **kwargs)
        self.fields['uid'].choices = PossibleUsers()
        self.fields['alias'].choices = PossibleAliases()


class AddAliasForm(forms.Form):
    common_name = forms.RegexField(regex="^[a-zA-Z\d\-_\$.]+$", required=True)
