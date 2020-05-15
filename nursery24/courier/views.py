from django.shortcuts import render,redirect
from django.db import IntegrityError
from django.contrib.auth.models import User,auth
from .models import Courier,Address
from http import cookies
from .forms import UserForm,AddressForm,CourierForm
from deliveryPersonnel.forms import UserForm as DForm
from deliveryPersonnel.forms import DeliveryPersonnelForm,UpdateForm
from django.core.exceptions import ObjectDoesNotExist
from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point
from deliveryPersonnel.models import DeliveryPersonnel
from django.db.models import Q
import datetime
from datetime import timedelta
from consumer.models import ProductInOrder
import json
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='../courier/login')
def home(request):
    return render(request,'cohome.html')

def signup(request):
    return render(request,'cosignup.html')

def signup_submit(request):
    try:
        if (request.method=='POST'):
            sname=request.POST["sname"]
            email=request.POST["mail"]
            uname=request.POST["uname"]
            pwd=request.POST["pwd"]
            phone=request.POST["phone"]
            addr=request.POST["address"]
            user=User.objects.create_user(email=email,username=uname,password=pwd)    
            courier=Courier(user=user,phone_number=phone,service_name=sname)
            courier.save()
            
            geolocator = Nominatim(user_agent="courier")
            location = geolocator.geocode(addr)
            address=Address(addr=addr,courier=courier,point=Point(location.latitude, location.longitude))
            address.save()
            user=auth.authenticate(username=uname,password=pwd)
            auth.login(request,user)
            return redirect('../courier/home')
    except IntegrityError as e:
        print('Username already exists')
        data={}
        data['msg']='Username already exists'
        return render(request,'cosignup.html',data)

def login(request):
    return render(request,'cologin.html')

def login_submit(request):
    if request.method=='POST':
        uname=request.POST["uname"]
        pwd=request.POST["pwd"]
        user=auth.authenticate(username=uname,password=pwd)
        if user is not None:
            try:
                courier=Courier.objects.get(user=user)
            except ObjectDoesNotExist as d:
                data={}
                data['msg']='User does not exist'
                return render(request,'cologin.html',data)
            else:
                auth.login(request,user)
                U = cookies.SimpleCookie()
                U['username'] = user
                
                return redirect('../courier/home')
        else:
            data={}
            data['msg']='Invalid Credentials'
            return render(request,'cologin.html',data)
    else:
        return render(request,'cologin.html')

def logout(request):
    auth.logout(request)
    print("Reached here")
    return redirect('../courier/login')

@login_required(login_url='../courier/login')
def myprofile(request):
    return render(request,'coprofile.html')

@login_required(login_url='../courier/login')
def edit(request):
    userform=UserForm()
    userform.fields['email'].initial=request.user.email
    courierform=CourierForm()
    courierform.fields['phone_number'].initial=Courier.objects.get(user=request.user).phone_number
    courierform.fields['service_name'].initial=Courier.objects.get(user=request.user).service_name
    return render(request,'coeditprofile.html',{'userform':userform,'courierform':courierform})

@login_required(login_url='../courier/login')
def editsubmit(request):
    if request.method=='POST':
        service_name=request.POST['service_name']
        email=request.POST['email']
        request.user.email=email
        request.user.save()
        phone_number=request.POST['phone_number']
        initial_profile_pic=request.user.courier.profile_pic.url
        initial_profile_pic=initial_profile_pic.replace('/media/', '')
        profile_pic=request.FILES['profile_pic'] if 'profile_pic' in request.FILES else initial_profile_pic
        courier=Courier.objects.get(user=request.user)
        courier.phone_number=phone_number
        courier.service_name=service_name
        courier.profile_pic = profile_pic
        courier.save()     
        return redirect('../courier/myprofile')  
    else: 
        return render(request,'coprofile.html')

@login_required(login_url='../courier/login')
def addresses(request):
    return render(request,'coaddress.html')

@login_required(login_url='../courier/login')
def addaddress(request):
    form=AddressForm()
    return render(request,'coaddaddress.html',{'form':form})

@login_required(login_url='../courier/login')
def addaddresssubmit(request):
    if request.method=='POST':
        courier_id=request.POST['courier']
        addr=request.POST['addr']
        courier=Courier.objects.get(pk=courier_id)

        geolocator = Nominatim(user_agent="courier")
        location = geolocator.geocode(addr)
        address=Address(addr=addr,courier=courier,point=Point(location.latitude, location.longitude))
        address.save()
        return redirect('../courier/addresses')

@login_required(login_url='../courier/login')
def removeaddresssubmit(request):
    if request.method=='POST':
        address_id=request.POST['id']
        Address.objects.get(pk=address_id).delete()
        return redirect('../courier/addresses')

@login_required(login_url='../courier/login')
def adddp(request):
    userform=DForm()
    delform=DeliveryPersonnelForm()
    return render(request,'coadddp.html',{'userform':userform,'delform':delform})

@login_required(login_url='../courier/login')
def adddpsubmit(request):
    if request.method=='POST':
        username=request.POST['username']
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        email=request.POST['email']
        user=User.objects.create_user(email=email,username=username,password='abc',first_name=fname,last_name=lname) 
        courier=request.user.courier   
        phone=request.POST['phone_number']
        profile_pic=request.FILES['profile_pic']
        dp=DeliveryPersonnel(user=user,courier=courier,phone_number=phone,profile_pic=profile_pic)
        dp.save()            
        return redirect('../courier/home')

@login_required(login_url='../courier/login')
def viewdp(request):
    if request.method=='POST':
        id=request.POST['id']
        dp=DeliveryPersonnel.objects.get(pk=id)
        return render(request,'coview.html',{'dp':dp})

@login_required(login_url='../courier/login')
def updatedp(request):
    if request.method=='POST':
        id=request.POST['id']
        dp=DeliveryPersonnel.objects.get(pk=id)
        updateform=UpdateForm()
        updateform.fields['first_name'].initial=dp.user.first_name
        updateform.fields['last_name'].initial=dp.user.last_name
        updateform.fields['email'].initial=dp.user.email
        delform=DeliveryPersonnelForm()
        delform.fields['phone_number'].initial=dp.phone_number
        return render(request,'coupdateprofile.html',{'updateform':updateform,'delform':delform,'id':id})

@login_required(login_url='../courier/login')
def updatedpsubmit(request):
    if request.method=='POST':
        id=request.POST['id']
        dp=DeliveryPersonnel.objects.get(pk=id)
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        phone_number=request.POST['phone_number']
        initial_profile_pic=dp.profile_pic.url
        initial_profile_pic=initial_profile_pic.replace('/media/', '')
        profile_pic=request.FILES['profile_pic'] if 'profile_pic' in request.FILES else initial_profile_pic
        dp.user.first_name=first_name
        dp.user.last_name=last_name
        dp.user.email=email
        dp.user.save()
        dp.phone_number=phone_number
        dp.profile_pic = profile_pic
        dp.save()     
        return redirect('../courier/home')  

@login_required(login_url='../courier/login')
def removedpsubmit(request):
    if request.method=='POST':
        user_id=request.POST['user_id']
        User.objects.filter(pk=user_id).delete()
        return redirect('../courier/home') 

@login_required(login_url='../courier/login')
def viewsummary(request):
    array=[]
    obj=request.user.courier.deliverypersonnel_set.all()
    for i in obj:
        c={}
        c['name']=i.user.first_name+' '+i.user.last_name
        c['D']=i.productinorder_set.filter(status='D').count()
        c['C']=i.productinorder_set.filter(Q(status='C') | Q(status='I') | Q(status='N')).count()
        array.append(c)
    return render(request,'cosummary.html',{'array':array})

@login_required(login_url='../courier/login')
def analyse(request):
    data={}
    if request.method=='POST':
        start_date=request.POST['from']
        t=request.POST['to']
    else:
        start_date=(datetime.datetime.now() + datetime.timedelta(-5)).strftime("%Y-%m-%d")
        t=datetime.datetime.now().strftime("%Y-%m-%d")
    
    end_date = (datetime.datetime.strptime(t, "%Y-%m-%d")+datetime.timedelta(1)).strftime("%Y-%m-%d")

    data['start_date']=start_date
    data['end_date']=t

    name=[]
    c=[]
    d=[]
    
    obj=request.user.courier.deliverypersonnel_set.all().order_by('user__first_name','user__last_name')
    for i in obj:
        name.append(i.user.first_name+' '+i.user.last_name)
        pio=i.productinorder_set.filter(last_tracked_on__range=(start_date,end_date))
        d.append(pio.filter(status='D').count())
        c.append(pio.filter(Q(status='C') | Q(status='I') | Q(status='N')).count())
        
    data['name']=json.dumps(name)
    data['c']=json.dumps(c)
    data['d']=json.dumps(d)
    return render(request,'coanalyse.html',data)
