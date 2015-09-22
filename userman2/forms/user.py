from django import forms


class ChfnForm(forms.Form):
    full_name = forms.RegexField(
        regex="^[^:^,]+$", error_message="Gecos entries may not contain : or ,")
    room_number = forms.RegexField(
        regex="^[^:^,]+$", required=False, error_message="Gecos entries may not contain : or ,")
    work_phone = forms.RegexField(
        regex="^[\d\-]+$", required=False, error_message="Phone numbers may only contain digits and -.")
    home_phone = forms.RegexField(
        regex="^[\d\-]+$", required=False, error_message="Phone numbers may only contain digits and -.")


class ChdescForm(forms.Form):
    description = forms.CharField(required=False)


class ChwarnRmForm(forms.Form):
    toBeDeleted = forms.DateTimeField(required=False)


class ChprivForm(forms.Form):
    server = forms.ChoiceField(
        choices=(("rob", "rob"), ("hendrik", "hendrik"), ("ank", "ank"), ("frans", "frans"), ("fw-01", "fw-01"),
                 ("gadgetlab", "gadgetlab")))
    service = forms.ChoiceField(
        choices=(("sshd", "sshd"), ("samba", "samba"), ("systemd-user", "systemd-user"), ("sudo", "sudo"),
                 ("cron", "cron"), ("vpn", "vpn")))


class ChshForm(forms.Form):
    login_shell = forms.ChoiceField(
        choices=(('/bin/bash', '/bin/bash'), ("/bin/zsh", "/bin/zsh"), ("/usr/bin/tcsh", "/usr/bin/tcsh"),
                 ("/bin/false", "/bin/false")))


class ChgroupForm(forms.Form):
    gid_number = forms.ChoiceField(choices=((100, 'users'), (50, 'staff')))


class ChHomeForm(forms.Form):
    new_directory = forms.RegexField(regex="^[a-zA-Z\d\/\-\_]+$")


class UsersForm(forms.Form):
    uid = forms.RegexField(regex="^[a-zA-Z\d \-\$]+$", required=False)
    cn = forms.RegexField(regex="^[^:^,]+$", required=False)
    uidnumber = forms.IntegerField(required=False)
    deleted = forms.BooleanField(required=False, initial=False)
    chlocal = forms.BooleanField(required=False, initial=False)
    anklocal = forms.BooleanField(required=False, initial=False)
    anksamba = forms.BooleanField(required=False, initial=False)
    nochlocal = forms.BooleanField(required=False, initial=False)
    noanklocal = forms.BooleanField(required=False, initial=False)
    noanksamba = forms.BooleanField(required=False, initial=False)


class AddUserForm(forms.Form):
    uid = forms.RegexField(
        regex="^[a-z][a-z\d\-$_]+$",
        error_message="UID entry must consist of alphanumeric characters, and be lower case")
    full_name = forms.RegexField(
        regex="^[^:^,]+$", error_message="Full name entry may not contain : or ,")
    access = forms.MultipleChoiceField(initial=('samba@ank',),
                                       choices=(('samba@ank', 'samba@ank'), ('sshd@rob', 'sshd@rob'),
                                                ('systemd-user@rob', 'systemd-user@rob')))


class ChpassForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
