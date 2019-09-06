from django import forms


class ChfnForm(forms.Form):
    full_name = forms.RegexField(
        regex="^[^:^,]+$", error_messages={'invalid': "Gecos entries may not contain : or ,"})
    room_number = forms.RegexField(
        regex="^[^:^,]+$", required=False, error_messages={'invalid': "Gecos entries may not contain : or ,"})
    work_phone = forms.RegexField(
        regex="^[\d\-]+$", required=False, error_messages={'invalid': "Phone numbers may only contain digits and -."})
    home_phone = forms.RegexField(
        regex="^[\d\-]+$", required=False, error_messages={'invalid': "Phone numbers may only contain digits and -."})


class ChdescForm(forms.Form):
    description = forms.CharField(required=False)


class ChwarnRmForm(forms.Form):
    toBeDeleted = forms.DateTimeField(required=False)


class ChprivForm(forms.Form):
    service = forms.ChoiceField(
        choices=(
            ("sshd@rob", "sshd@rob"),
            ("systemd-user@rob", "systemd-user@rob"),
            ("sshd@hendrik", "sshd@hendrik"),
            ("systemd-user@hendrik", "systemd-user@hendrik"),
            ("samba@ank", "samba@ank"),
            ("vpn@fw-01", "vpn@fw-01")
        )
    )


class ChshForm(forms.Form):
    login_shell = forms.ChoiceField(
        choices=(
            ("/bin/bash", "/bin/bash"),
            ("/bin/zsh", "/bin/zsh"),
            ("/usr/bin/fish", "/usr/bin/fish"),
            ("/bin/false", "/bin/false"),
        )
    )


class ChgroupForm(forms.Form):
    gid_number = forms.ChoiceField(choices=((100, 'users'), (50, 'staff')))


class ChHomeForm(forms.Form):
    new_directory = forms.RegexField(regex="^[a-zA-Z\d\/\-\_]+$")


class AddUserForm(forms.Form):
    uid = forms.RegexField(
        regex="^[a-z][a-z\d\-$_]+$",
        error_messages={'invalid': "UID entry must consist of alphanumeric characters, and be lower case"})
    full_name = forms.RegexField(
        regex="^[^:^,]+$", error_messages={'invalid': "Full name entry may not contain : or ,"})
    access = forms.MultipleChoiceField(
        initial=('samba@ank',),
        choices=(
            ('samba@ank', 'samba@ank'),
            ('sshd@rob', 'sshd@rob'),
            ('systemd-user@rob', 'systemd-user@rob')
        )
    )
