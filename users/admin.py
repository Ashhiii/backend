from django.contrib import admin
from .models import User
from .models import Admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_admin')  # 👈 Add is_admin
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('first_name',)

admin.site.register(Admin)