from django import forms
from userman2.model import user
from userman2.model import alias

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

# The choices property of ChoiceField evaluates the choices field with a list(),
# such that the iterator is only evaluated once. We don't want that, so we
# override the property here.
class NoCacheChoiceField(forms.ChoiceField):
    def _get_choices(self):
        return self._choices

    def _set_choices(self, value):
        self._choices = self.widget.choices = value

    choices = property(_get_choices, _set_choices)

class AliasForm(forms.Form):
    uid = forms.RegexField(regex="^[@.a-zA-Z\d\-_]+$", required=False)
    cn = forms.RegexField(regex="^[^:^,]+$", required=False)

class AddUserForm(forms.Form):
    uid = NoCacheChoiceField(choices=PossibleUsers(), required=False)
    alias = NoCacheChoiceField(choices=PossibleAliases(), required=False)
    email = forms.EmailField (required=False)

class AddAliasForm(forms.Form):
    common_name = forms.RegexField(regex="^[a-zA-Z\d\-_\$.]+$", required=True)
