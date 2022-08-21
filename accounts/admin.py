from django.contrib import admin
from .models import User    
from django.contrib.auth.admin import UserAdmin

class UserAdmin(admin.ModelAdmin):
    fields = ('email', ('first_name', 'last_name'), 'town', 'birth_date', 'answer_count')
    readonly_fields = ('email', 'first_name', 'last_name', 'town', 'birth_date', 'answer_count')
    list_display = ('first_name', 'last_name', 'answer_count')
    search_fields = ('first_name', 'last_name')

admin.site.register(User, UserAdmin)