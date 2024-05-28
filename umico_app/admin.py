from django.contrib import admin
from .models import Address, Customer, Print, Scan, Frame

# Register your models here.
admin.site.register(Address)
admin.site.register(Customer)
admin.site.register(Print)
admin.site.register(Scan)
admin.site.register(Frame)
