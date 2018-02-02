from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'birth_date')


admin.site.register(Profile, ProfileAdmin)
