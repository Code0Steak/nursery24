from django.db import models
from django.contrib.gis.db import models as gismodel
from django.contrib.auth.models import User
from courier.models import Courier
from provider.models import Provider,Product
from deliveryPersonnel.models import DeliveryPersonnel

class Consumer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=10,blank=False)
    profile_pic=models.ImageField(upload_to='dps/',default='dps/profile.png')

class Address(models.Model):
    addr=models.TextField(max_length=100,null=True)
    point = gismodel.PointField(null=True)
    consumer=models.ForeignKey(Consumer,on_delete=models.CASCADE)

class Order(models.Model):
    total_price=models.IntegerField()
    secondary_id=models.CharField(max_length=8,blank=False)
    date_placed=models.DateTimeField(null=True)
    consumer=models.ForeignKey(Consumer,on_delete=models.CASCADE,null=True)
    delivery_addr=models.TextField(max_length=100,null=True)
    delivery_point = gismodel.PointField(null=True)
    
class ProductInOrder(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    provider=models.ForeignKey(Provider,on_delete=models.CASCADE)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField(null=True)
    total_price=models.IntegerField(null=True)
    ORDER_STATUS_CHOICES=[
        ('D','Delivered'),
        ('S','Shipped'),
        ('P','Placed'),
        ('C','Cancelled'),
        ('R','Ready To Ship'),
        ('N','Not Returned'),
        ('I','Inform Courier about cancellation')
    ]
    status=models.CharField(max_length=1,choices=ORDER_STATUS_CHOICES,default='P')
    expected_delivery_date=models.DateTimeField(null=True)
    date_delivered=models.DateTimeField(null=True)
    last_tracked_on=models.DateTimeField(null=True)
    last_tracked_by=models.ForeignKey(DeliveryPersonnel,on_delete=models.CASCADE,null=True)
    provider_addr=models.TextField(max_length=100,null=True)
    provider_point = gismodel.PointField(null=True)
    
class Review(models.Model):
    rating=models.FloatField()
    consumer=models.OneToOneField(Consumer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True) 