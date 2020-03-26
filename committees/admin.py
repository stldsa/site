from django.contrib import admin
from .models import Committee, Person

# Register your models here.
admin.site.register(Person)
admin.site.register(Committee)
