from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserRegistration)
admin.site.register(Login)
admin.site.register(Message)