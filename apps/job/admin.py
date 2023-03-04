from django.contrib import admin

from .models import Category, Item, Job, JobApplication, Section

admin.site.register(Job)
admin.site.register(Category)
admin.site.register(Section)
admin.site.register(Item)
admin.site.register(JobApplication)
