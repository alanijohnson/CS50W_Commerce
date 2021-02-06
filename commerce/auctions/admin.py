from django.contrib import admin
from .models import User, Category, Tag, UserProfile, Listing, Bid, Comment
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display_links = ['username']
    search_fields = ('username','email','date_joined','is_admin')
    ordering = ('username','email','date_joined','is_admin')
    list_display = ('is_admin','username','email','date_joined','is_superuser')
    list_filter = ('username','email','date_joined','is_admin')
    fieldsets = (
        (None, {'fields': ('username', 'password','email')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    
# extend from admin.ModelAdmin for models
    
admin.site.register(User,CustomUserAdmin)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Listing)
admin.site.register(Tag)
admin.site.register(Bid)
admin.site.register(Comment)
