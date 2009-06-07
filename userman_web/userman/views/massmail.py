from userman.model import user
from userman.model import group
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.cache import cache_control
from django.conf import settings

from userman.forms.massmail import *
from email.MIMEText import MIMEText
import smtplib

@cache_control(no_cache=True, must_revalidate=True)
def selectUsers(request):
    if (request.GET):
	form = MassMailForm(request.GET)
	if form.is_valid():
	    # Add all users, or just the selected groups
	    if not form.cleaned_data["groups"] and not form.cleaned_data["users"]:
		users = user.GetAllUsers(form.cleaned_data)
	    else: 
		usernames = set(form.cleaned_data["users"])
		for groupname in form.cleaned_data["groups"]:
		    usernames |= set(group.FromCN(groupname).members)
		users = [ user.FromUID (username) for username in usernames ]
	    
	    # Filter excluded users
	    excluded_users = set(form.cleaned_data["excludedusers"])
	    for groupname in form.cleaned_data["excludedgroups"]:
		excluded_users |=  set(group.FromCN(groupname).members)
	    def f(x): return x.uid not in excluded_users
	    users = filter(f, users)
	else:
    	    users = user.GetAllUsers()
    else:
	form = MassMailForm()
	users = user.GetAllUsers()

    count = {"total":len(users)}
    
    return render_to_response('massmail.html', {'users': users, 'form': form, 'count': count})

def writeMail(request):
    usernames = []
    if request.GET:
	form = WriteMailForm(request.GET)
	if form.is_valid():
	    if not form.cleaned_data["users"]:
		return HttpResponseRedirect('/userman2/massmail/')
	    usernames = form.cleaned_data["users"]
	    
    return render_to_response('massmail2.html', {'form': form, 'users': usernames})

def sendMail(request):
    usernames = []
    if request.GET:
	form = SendMailForm(request.GET)
	if form.is_valid():
	    usernames = form.cleaned_data["users"]
	    if form.cleaned_data["reallysend"]:
		for user in form.cleaned_data['users']:
		    msg = MIMEText(form.cleaned_data["body"])
		    msg['Subject'] = form.cleaned_data["subject"]
		    msg['From'] = form.cleaned_data["fromaddress"]
		    msg['To'] = user + "@ch.tudelft.nl"
    		    print msg;
		    s = smtplib.SMTP()
	    	    s.connect()
	    	    s.sendmail(form.cleaned_data["fromaddress"], [user + "@ch.tudelft.nl"], msg.as_string())
	    	    s.close()
		return HttpResponseRedirect('/userman2/massmail/')
    	    return render_to_response('massmail3.html', {'form': form, 'users': usernames, 'fromaddress': form.cleaned_data['fromaddress'], 'subject': form.cleaned_data['subject'], 'body': form.cleaned_data['body'], 'removaldate': form.cleaned_data['removal_date']})
	
    return HttpResponseRedirect('/userman2/massmail/')
