from django.contrib import admin
from .models import asset, teacher, student, assetevent

# Register your models here.

admin.site.register(teacher)
admin.site.register(student)
admin.site.register(asset)
admin.site.register(assetevent)

