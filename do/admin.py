from django.contrib import admin
from .models import todo


class todoAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)


admin.site.register(todo, todoAdmin)
