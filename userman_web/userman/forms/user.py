from django import newforms as forms

class ChfnForm(forms.Form):
    full_name = forms.RegexField(regex="^[^:^,]+$", error_message="Gecos entries may not contain : or ,")
    room_number = forms.RegexField(regex="^[^:^,]+$", required=False, error_message="Gecos entries may not contain : or ,")
    work_phone = forms.RegexField(regex="^[\d\-]+$", required=False, error_message="Phone numbers may only contain digits and -.")
    home_phone = forms.RegexField(regex="^[\d\-]+$", required=False, error_message="Phone numbers may only contain digits and -.")

class ChdescForm(forms.Form):
    description = forms.CharField(required=False)

class ChprivForm(forms.Form):
    server = forms.ChoiceField(choices=(("frans", "frans"), ("ank", "ank"), ("ch", "ch")))
    service = forms.ChoiceField(choices=(("ssh", "ssh"), ("samba", "samba")))

class ChshForm(forms.Form):
    login_shell = forms.ChoiceField(choices=(('/bin/bash','/bin/bash'), ("/usr/bin/tcsh", "/usr/bin/tcsh"), ("/bin/false", "/bin/false")))

class ChgroupForm(forms.Form):
    gid_number = forms.ChoiceField(choices=((100,'users'), (50,'staff')))

class UsersForm(forms.Form):
    uid = forms.RegexField(regex="^[a-zA-Z\d \-\$]+$", required=False)
    cn = forms.RegexField(regex="^[^:^,]+$", required=False)
    uidnumber = forms.IntegerField(required=False)
    deleted = forms.BooleanField(required=False, initial=False)
    chlocal = forms.BooleanField(required=False, initial=False)
    chsamba = forms.BooleanField(required=False, initial=False)
    anklocal = forms.BooleanField(required=False, initial=False)
    anksamba = forms.BooleanField(required=False, initial=False)
    nochlocal = forms.BooleanField(required=False, initial=False)
    nochsamba = forms.BooleanField(required=False, initial=False)
    noanklocal = forms.BooleanField(required=False, initial=False)
    noanksamba = forms.BooleanField(required=False, initial=False)
