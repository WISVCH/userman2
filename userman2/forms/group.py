from django import forms
from userman2.model import user
import choicefield

class GroupsForm(forms.Form):
    uid = forms.RegexField(regex="^[a-zA-Z\d \-\$]+$", required=False)
    cn = forms.RegexField(regex="^[^:^,]+$", required=False)

class AddUserForm(forms.Form):
    possibleUsers = [ (username, username) for username in user.GetAllUserNames() ]
    user = choicefield.NoCacheChoiceField(choices=possibleUsers)
    
class AddGroupForm(forms.Form):
    common_name = forms.RegexField(regex="^[a-z\d\-_]+$", required=True)
