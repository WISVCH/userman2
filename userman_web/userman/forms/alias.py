from django import newforms as forms
from userman.model import user
from userman.model import alias

class AliasForm(forms.Form):
    uid = forms.RegexField(regex="^[a-zA-Z\d \-\$]+$", required=False)
    cn = forms.RegexField(regex="^[^:^,]+$", required=False)

class AddUserForm(forms.Form):
    possibleUsers = [("","")]
    possibleUsers += [ (username, username) for username in user.GetAllUserNames() ]
    uid = forms.ChoiceField(choices=possibleUsers, required=False)
    
    possibleAliases = [("","")]
    possibleAliases += [ (username, username) for username in alias.getAllAliasNames() ]
    alias = forms.ChoiceField(choices=possibleAliases, required=False)

    email = forms.EmailField (required=False)

class AddAliasForm(forms.Form):
#    possibleUsers = [ (username, username) for username in user.getAllUserNames() ]
    common_name = forms.RegexField(regex="^[a-zA-Z\d\-_\$]+$", required=True)
        