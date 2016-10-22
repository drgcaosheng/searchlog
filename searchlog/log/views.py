from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse,Http404
from django import forms
from django.contrib import auth
from django.http import HttpResponseRedirect
import datetime
from django.contrib.admin import widgets
import subprocess
import os.path


class loginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

class searchForm(forms.Form):
    searchform = forms.CharField(label="Please Enter Search Content",min_length=1)
    day = forms.DateTimeField(label='Please Enter Log Date',widget=widgets.AdminDateWidget())

def login(request):
    error = False
    if request.method == 'POST':
        #print 'ttttt'
        form = loginForm(request.POST)
        #print '223333333333333333333'
        if form.is_valid():
            #print '222222222'
            username = request.POST.get('username','')
            password = request.POST.get('password','')
            user = auth.authenticate(username=username,password=password)
            #uf = form.cleaned_data
            if user is not None and user.is_active:
                #print '1'
                auth.login(request,user)
                return HttpResponseRedirect("/loginsuccess/")
            else:
                #print '2'
                error=True  
                #return HttpResponse("not user")
    else:
        form = loginForm()
    return render_to_response('login.html',{'form':form,'error':error})

def loginsuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            searchform = searchForm(request.POST)
            if searchform.is_valid():
                searchtext = searchform.cleaned_data['searchform']
                today = searchform.cleaned_data['day']
                today_day = str(today.day).zfill(2)
                #print today_day
                #print searchtext
                if '|' in searchtext:
                    searchtext_error = True
                    return render_to_response('search.html',{'form':searchform,'searchtext_error':searchtext_error})
                logpath = os.path.join('/home/var/log/',str(today.year),str(today.month),today_day)
                if not os.path.exists(logpath):
                    file_error = True
                    return render_to_response('search.html',{'form':searchform,'file_error':file_error})
                logpath = os.path.join(logpath,'*')
                cmd = "sudo grep %s %s"%(searchtext,logpath)
                #print cmd
                showlog = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
                text = showlog.communicate()
                textshow = text[0].split('\n')
                #print textshow
                return render_to_response('search.html',{'showlog':textshow,'form':searchform})
                #return render_to_response('showlog.html',{'showlog':textshow})
                #return HttpResponse(textshow)
        else:
            searchform = searchForm(
                initial={'day':datetime.datetime.now().strftime("%Y-%m-%d")}
            )
        return render_to_response('search.html',{'form':searchform})
        
        #return HttpResponse("OK")
    else:
        #return HttpResponse("NO")
        return HttpResponseRedirect("/login/")

def logout(request):
    auth.logout(request)
    #return HttpResponse("quit")
    return render_to_response("logout.html")
