from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.models import User,auth
from django.core.exceptions import ObjectDoesNotExist
from .models import DeliveryPersonnel

# Create your views here.
def home(request):
    return render(request,'dhome.html')

def login(request):
    return render(request,'dlogin.html')

def login_submit(request):
    if request.method=='POST':
        uname=request.POST["uname"]
        pwd=request.POST["pwd"]
        user=auth.authenticate(username=uname,password=pwd)
        if user is not None:
            try:
                dp=DeliveryPersonnel.objects.get(user=user)
            except ObjectDoesNotExist as d:
                return HttpResponse('User does not exist')
            else:
                auth.login(request,user)
                return redirect('../delivery/home')
        else:
            return HttpResponse('Invalid Credentials')
    else:
        return render(request,'login')

def logout(request):
    auth.logout(request)
    print("Reached here")
    return redirect('../delivery/login')

def myprofile(request):
    return render(request,'dprofile.html')

def changepassword(request):
    return render(request,'dchange.html')

def changepasswordsubmit(request):
    if request.method=='POST':
        uname=request.POST["user"]
        prev=request.POST["prev"]
        new=request.POST["new"]
        cnf=request.POST["cnf"]
        if (uname!=request.user.username):
            return HttpResponse("Wrong Username")
        elif not (request.user.check_password(prev)):
            return HttpResponse("Wrong Password")
        elif (new!=cnf):
            return HttpResponse("Passwords don't match")
        else:
            request.user.set_password(new)
            request.user.save()
            user=auth.authenticate(username=uname,password=new)
            auth.login(request,user)
            return redirect('../delivery/home')