from django import forms
from userman.model import user
from userman.model import group


class MassMailForm(forms.Form):
    uid = forms.RegexField(regex="^[a-zA-Z\d \-\$]+$", required=False)
    cn = forms.RegexField(regex="^[^:^,]+$", required=False)

    supergroups = group.GetAllGroups()
    possibleGroups = []
    for groups in supergroups.items():
	possibleGroups += [ (group.cn, group.cn) for group in groups[1] ]
	possibleGroups.sort()
	
    groups = forms.MultipleChoiceField(required=False, choices=possibleGroups)
    excludedgroups = forms.MultipleChoiceField(required=False, choices=possibleGroups)

    possibleUsers = [ (username, username) for username in user.GetAllUserNames() ]         
    users = forms.MultipleChoiceField(required=False, choices=possibleUsers)
    excludedusers = forms.MultipleChoiceField(required=False, choices=possibleUsers)

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
    
class WriteMailForm(forms.Form):
    possibleUsers = [ (username, username) for username in user.GetAllUserNames() ]         
    users = forms.MultipleChoiceField(required=True, widget=forms.MultipleHiddenInput, choices=possibleUsers)
    fromaddress = forms.EmailField(required=True)
    subject = forms.CharField(required=False)
    body = forms.CharField(required=False, widget=forms.Textarea)
    removaldue = forms.IntegerField(required=False)
    removalunits = forms.ChoiceField(required=False, choices=[('weeks', 'weeks'),('days', 'days'), ('months', 'months')])
    
class SendMailForm(forms.Form):
    possibleUsers = [ (username, username) for username in user.GetAllUserNames() ]         
    users = forms.MultipleChoiceField(required=True, widget=forms.MultipleHiddenInput, choices=possibleUsers)
    fromaddress = forms.EmailField(required=True, widget=forms.HiddenInput)
    subject = forms.CharField(required=True, widget=forms.HiddenInput)
    body = forms.CharField(required=True, widget=forms.HiddenInput)
    removaldate = forms.DateField(required=False, widget=forms.HiddenInput)
    reallysend = forms.BooleanField(required=False)
