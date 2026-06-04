from django.contrib import admin

# Regifrom django.contrib import admin
from .models import Customer, Policy, Claim

admin.site.register(Customer)
admin.site.register(Policy)
admin.site.register(Claim)
