from django.contrib import admin
from .models import Account, Location, Category, Impact

# Register your models here.
admin.site.register(Account)
admin.site.register(Location)
admin.site.register(Category)
admin.site.register(Impact)