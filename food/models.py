from django.db import models
from django.conf import settings

# Create your models here.
class Restaurants(models.Model):
   
    res_name = models.CharField(max_length=50)
    res_desc = models.CharField(max_length=300)
    res_address = models.CharField(max_length=100)
    pub_date = models.DateField()
    res_image = models.ImageField(upload_to="food/images", default="")

    def __str__(self):
        return self.res_name

class Dishes(models.Model):
    restaurant = models.ForeignKey(Restaurants, on_delete=models.CASCADE)
    dish_name = models.CharField(max_length=50)
    dish_desc = models.CharField(max_length = 300)
    dish_price = models.IntegerField(default=0)
    category = models.CharField(max_length=50, default="")
    
    pub_date = models.DateField()
    dish_image = models.ImageField(upload_to="food/images", default="")

    def __str__(self):
        return self.dish_name

class Contact(models.Model):
    name = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 100)
    phone = models.IntegerField()
    message = models.TextField(max_length=300)

    def __str__(self):
        return self.name


class OrderDetail(models.Model):
    order_no    = models.CharField(max_length=100,default="")
    amount      = models.FloatField(default=0)
    user_id     = models.IntegerField(default=0)
    name        = models.CharField(max_length = 50,default="")
    email       = models.CharField(max_length = 50,default="")
    address     = models.CharField(max_length = 100,default="")
    address2    = models.CharField(max_length = 100,default="")
    city        = models.CharField(max_length = 20,default="")
    state       = models.CharField(max_length = 20,default="")
    zipcode     = models.CharField(max_length = 10,default="")
    mobile      = models.CharField(max_length = 20,default="")

class OrderItem(models.Model):
    order_no    = models.CharField(max_length=100,default="")
    dish_id     = models.IntegerField(default=0)
   
    quantity    = models.FloatField(default=0)
    price       = models.FloatField(default=0)