from django.contrib import admin
from .models import User    
from django.contrib.auth.admin import UserAdmin

@admin.action(description='Block')
def block(modeladmin, request, queryset):
    queryset.update(status='b')

@admin.action(description='Make active')
def activate(modeladmin, request, queryset):
    queryset.update(status='a')


class UserAdmin(admin.ModelAdmin):
    fields = ('email', ('first_name', 'last_name'), 'town', 'birth_date', 'answer_count', 'status')
    readonly_fields = ('email', 'first_name', 'last_name', 'town', 'birth_date', 'answer_count', 'status')
    list_display = ('first_name', 'last_name', 'answer_count')
    search_fields = ('first_name', 'last_name')
    actions = [block, activate]

admin.site.register(User, UserAdmin)