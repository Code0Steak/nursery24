from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.models import User,auth
from .models import Address,Provider,Product
from .forms import AddressForm,ProductForm,PriceForm,UserForm,ProviderForm
from django.core.exceptions import ObjectDoesNotExist
from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point
from consumer.models import ProductInOrder
from datetime import date
from deliveryPersonnel.models import DeliveryPersonnel

# Create your views here.
def signup(request):
    return render(request,'psignup.html')

def signup_submit(request):
    try:
        if (request.method=='POST'):
            fname=request.POST["fname"]
            lname=request.POST["lname"]
            email=request.POST["mail"]
            uname=request.POST["uname"]
            pwd=request.POST["pwd"]
            phone=request.POST["phone"]
            addr=request.POST["address"]
            shop=request.POST["shop_name"]
            user=User.objects.create_user(first_name=fname,last_name=lname,email=email,username=uname,password=pwd)    
            provider=Provider(user=user,phone_number=phone,shop_name=shop)
            provider.save()

            geolocator = Nominatim(user_agent="provider")
            location = geolocator.geocode(addr)
            address=Address(addr=addr,provider=provider,point=Point(location.latitude, location.longitude))
            address.save()

            user=auth.authenticate(username=uname,password=pwd)
            auth.login(request,user)
            return redirect('../provider/home')
    except IntegrityError as e:
        return HttpResponse ('Username already exists')

def login(request):
    return render(request,'plogin.html')

def login_submit(request):
    if request.method=='POST':
        uname=request.POST["uname"]
        pwd=request.POST["pwd"]
        user=auth.authenticate(username=uname,password=pwd)
        if user is not None:
            try:
                provider=Provider.objects.get(user=user)
            except ObjectDoesNotExist as d:
                return HttpResponse('User does not exist')
            else:
                auth.login(request,user)
                return redirect('../provider/home')
        else:
            return HttpResponse('Invalid Credentials')
    else:
        return render(request,'login')

def logout(request):
    auth.logout(request)
    return redirect ('../provider/login')

def home(request):
    list=request.user.provider.productinorder_set.all().filter(status='P').order_by('order__date_placed')
    return render(request,'phome.html',{'list':list})

def additem(request):
    productform=ProductForm()
    priceform=PriceForm()
    return render(request,'padditem.html',{'productform':productform,'priceform':priceform})

def additemsubmit(request):
    if request.method=='POST':
        provider_id=request.POST['provider']
        name=request.POST['name']
        image=request.FILES['image']
        category=request.POST['category']
        price=request.POST['price']
        provider=Provider.objects.get(pk=provider_id)
        try:
            check_product=Product.objects.get(name=name)
        except ObjectDoesNotExist as d:
            product=Product(image=image,name=name,category=category)
            product.save()
            product.providers.add(provider,through_defaults={'price':price})
        else:
            check_product.providers.add(provider,through_defaults={'price':price})
        return redirect('../provider/removeitem')

def removeitem(request):
    return render(request,'premoveitem.html')

def removeitemsubmit(request):
    if (request.method=='POST'):
        product_id=request.POST['id']
        provider_id=request.POST['proid']
        product=Product.objects.get(pk=product_id)
        provider=Provider.objects.get(pk=provider_id)
        provider.product_set.remove(product)
        return redirect('../provider/removeitem')

def addbranch(request):
    form=AddressForm()
    return render(request,'paddbranch.html',{'form':form})

def myprofile(request):
    return render(request,'pprofile.html')

def addbranchsubmit(request):
    if request.method=='POST':
        provider_id=request.POST['provider']
        addr=request.POST['addr']
        provider=Provider.objects.get(pk=provider_id)
        geolocator = Nominatim(user_agent="provider")
        location = geolocator.geocode(addr)
        address=Address(addr=addr,provider=provider,point=Point(location.latitude, location.longitude))
        address.save()
        return redirect('../provider/removebranch')

def removebranch(request):
    return render(request,'premovebranch.html')

def removebranchsubmit(request):
    if request.method=='POST':
        address_id=request.POST['id']
        Address.objects.get(pk=address_id).delete()
        return redirect('../provider/removebranch')

def edit(request):
    userform=UserForm()
    userform.fields['first_name'].initial=request.user.first_name
    userform.fields['last_name'].initial=request.user.last_name
    userform.fields['email'].initial=request.user.email
    providerform=ProviderForm()
    providerform.fields['phone_number'].initial=Provider.objects.get(user=request.user).phone_number
    providerform.fields['shop_name'].initial=Provider.objects.get(user=request.user).shop_name
    return render(request,'peditprofile.html',{'userform':userform,'providerform':providerform})

def editsubmit(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        request.user.first_name=first_name
        request.user.last_name=last_name
        request.user.email=email
        request.user.save()
        phone_number=request.POST['phone_number']
        shop_name=request.POST['shop_name']
        initial_profile_pic=request.user.provider.profile_pic.url
        initial_profile_pic=initial_profile_pic.replace('/media/', '')
        profile_pic=request.FILES['profile_pic'] if 'profile_pic' in request.FILES else initial_profile_pic
        provider=Provider.objects.get(user=request.user)
        provider.phone_number=phone_number
        provider.profile_pic=profile_pic
        provider.shop_name=shop_name
        provider.save()
        return redirect('../provider/myprofile')  
    else: 
        return render(request,'pprofile.html')  

def readytoship(request):
    if request.method=='POST':
        id=request.POST['id']
        return render(request,'pselectaddress.html',{'productinorderid':id})

def readytoshipsubmit(request):
    if request.method=='POST':
        id=request.POST['id']
        addr=request.POST['addr']
        product=ProductInOrder.objects.get(pk=id)
        product.status='R'
        product.last_tracked_on=date.today()

        #static now
        #change later
        dp=DeliveryPersonnel.objects.get(id=8)
        dp.assigned=True
        dp.save()
        product.last_tracked_by=dp

        geolocator = Nominatim(user_agent="provider")
        location = geolocator.geocode(addr)
        
        product.provider_addr=addr
        product.provider_point=Point(location.latitude, location.longitude)
        product.save()
        return redirect('../provider/home')

def ready(request):
    list=request.user.provider.productinorder_set.all().filter(status='R').order_by('order__date_placed')
    return render(request,'pready.html',{'list':list})