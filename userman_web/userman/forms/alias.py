from django import newforms as forms
from userman.model import user
from userman.model import alias

# The code under AddUserForm is only evaluated once at start-up, so if
# we create the list of choices there it will never be changed even if
# we add/remove items. The iterables below will be evaluated everytime
# the form is displayed.
class PossibleUsers:
    def __iter__(self):
        return iter([("","")] + [ (username, username) for username in user.GetAllUserNames() ])

class PossibleAliases:
    def __iter__(self):
        return iter( [("","")] + [ (username, username) for username in alias.getAllAliasNames() ])

class AliasForm(forms.Form):
    uid = forms.RegexField(regex="^[@.a-zA-Z\d\-_]+$", required=False)
    cn = forms.RegexField(regex="^[^:^,]+$", required=False)

class AddUserForm(forms.Form):
    uid = forms.ChoiceField(choices=PossibleUsers(), required=False)
    alias = forms.ChoiceField(choices=PossibleAliases(), required=False)
    email = forms.EmailField (required=False)

class AddAliasForm(forms.Form):
    common_name = forms.RegexField(regex="^[a-zA-Z\d\-_\$.]+$", required=True)
