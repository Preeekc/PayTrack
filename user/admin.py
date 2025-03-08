from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Customizing the UserAdmin for the CustomUser model
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Fields to display in the admin list view
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    # Fields to filter in the admin view
    list_filter = ('user_type', 'is_staff', 'is_active')
    # Fields to use for editing/creating a user in the admin form
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('User Type', {'fields': ('user_type',)}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
    )
    # Fields to use for creating a user in the admin form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type', 'is_staff', 'is_active'),
        }),
    )
    # Fields to search for in the admin view
    search_fields = ('username', 'email')
    ordering = ('username',)

# Register the CustomUser model with the customized admin interface
admin.site.register(CustomUser, CustomUserAdmin)


from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'property_type', 'price', 'featured', 'homeowner')
    list_filter = ('property_type', 'location', 'featured', 'homeowner')
    search_fields = ('title', 'location', 'description', 'homeowner__email', 'homeowner__username')
    list_editable = ('featured',)  # Allow toggling 'featured' directly in the admin
    
    # Optional: Add a filter to only show home owners in the dropdown
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "homeowner":
            kwargs["queryset"] = db_field.related_model.objects.filter(user_type='home owner')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)