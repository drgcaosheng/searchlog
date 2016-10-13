from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django import forms
from django.contrib import auth
from django.http import HttpResponseRedirect

class loginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

class searchForm(forms.Form):
    searchform = forms.CharField(min_length=5)

def login(request):
    error = True
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username','')
            password = request.POST.get('password','')
            print username
            print password 
            user = auth.authenticate(username=username,password=password)
            #uf = form.cleaned_data
            #print uf
            if user is not None and user.is_active:
            
                auth.login(request,user)
                return HttpResponseRedirect("/loginsuccess/")
            else:
                error = True
                #return HttpResponse("not user")
                return render_to_response('login.html',{'form':form,'error':error})
            #return HttpResponse("OK")
    else:
        error = False
        form = loginForm()
    	return render_to_response('login.html',{'form':form,'error':error})

def loginsuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            searchform = searchForm(request.POST)
            if searchform.is_valid():
                print searchform.cleaned_data
                return HttpResponse('searchsuccess')
        else:
            searchform = searchForm()
        return render_to_response('search.html',{'form':searchform})
        #return HttpResponse("OK")
    else:
        #error = True
        #form = loginForm()
        return HttpResponseRedirect("/login/")
        #return HttpResponse("NO")

def logout(request):
    auth.logout(request)
    return HttpResponse("quit")
