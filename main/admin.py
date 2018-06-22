from django.contrib import admin
from .models import User, Group

# Register your models here.
simple_registers = [User, Group]
for to_register in simple_registers:
    admin.site.register(to_register)
