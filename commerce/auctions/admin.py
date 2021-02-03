from django.contrib import admin
from .models import User, Category, Tag, UserProfile, Listing
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display_links = []
    search_fields = ('username','email','first_name','last_name','date_joined','is_admin')
    ordering = ('username','first_name','last_name','email','date_joined','is_admin')
    list_display = ('is_admin','username','first_name','last_name','email','date_joined','is_superuser')
    list_filter = ('username','email','date_joined','is_admin')
    fieldsets = (
        (None, {'fields': ('username', 'password','email','first_name','last_name')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    
# extend from admin.ModelAdmin for models
    
admin.site.register(User,CustomUserAdmin)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Listing)
admin.site.register(Tag)
