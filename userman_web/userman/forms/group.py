from django import newforms as forms
from userman.model import user

#class ChfnForm(forms.Form):
#    full_name = forms.RegexField(regex="^[^:^,]+$", error_message="Gecos entries may not contain : or ,")
#    room_number = forms.RegexField(regex="^[^:^,]+$", required=False, error_message="Gecos entries may not contain : or ,")
#    work_phone = forms.RegexField(regex="^[\d\-]+$", required=False, error_message="Phone numbers may only contain digits and -.")
#    home_phone = forms.RegexField(regex="^[\d\-]+$", required=False, error_message="Phone numbers may only contain digits and -.")

#class ChdescForm(forms.Form):
#    description = forms.CharField(required=False)

#class ChshForm(forms.Form):
#    login_shell = forms.ChoiceField(choices=(('/bin/bash','/bin/bash'), ("/usr/bin/tcsh", "/usr/bin/tcsh"), ("/bin/false", "/bin/false")))

#class ChgroupForm(forms.Form):
#    gid_number = forms.ChoiceField(choices=((100,'users'), (50,'staff')))

class GroupsForm(forms.Form):
    uid = forms.RegexField(regex="^[a-zA-Z\d \-\$]+$", required=False)
    cn = forms.RegexField(regex="^[^:^,]+$", required=False)

class AddUserForm(forms.Form):
    possibleUsers = [ (username, username) for username in user.getAllUserNames() ]
    user = forms.ChoiceField(choices=possibleUsers)
    
class AddGroupForm(forms.Form):
    common_name = forms.RegexField(regex="^[a-zA-Z\d\-_]+$", required=True)
