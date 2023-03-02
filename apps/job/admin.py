from django.contrib import admin

from .models import Category, Item, Job, Section

admin.site.register(Job)
admin.site.register(Category)
admin.site.register(Section)
admin.site.register(Item)
