from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Item, Cart, Order

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['id', 'email', 'name', 'city', 'is_customer', 'is_seller', 'is_staff', 'is_active']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'city')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_customer', 'is_seller', 'groups', 'user_permissions'),
        }),
        (_('Important Dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'city', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'name')
    list_filter = ('is_customer', 'is_seller', 'is_staff', 'is_superuser', 'groups')

    filter_horizontal = ('groups', 'user_permissions')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','price', 'category')  
    search_fields = ('name', 'category')               
    list_filter = ('category',)                         


admin.site.register(User, UserAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Cart)
admin.site.register(Order)