from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Restaurants)
admin.site.register(Dishes)
admin.site.register(Contact)
admin.site.register(OrderDetail)
admin.site.register(OrderItem)