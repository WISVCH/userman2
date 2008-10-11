from django import forms
from userman.model import user

class GroupsForm(forms.Form):
    uid = forms.RegexField(regex="^[a-zA-Z\d \-\$]+$", required=False)
    cn = forms.RegexField(regex="^[^:^,]+$", required=False)

class AddUserForm(forms.Form):
    possibleUsers = [ (username, username) for username in user.GetAllUserNames() ]
    user = forms.ChoiceField(choices=possibleUsers)
    
class AddGroupForm(forms.Form):
    common_name = forms.RegexField(regex="^[a-zA-Z\d\-_]+$", required=True)
