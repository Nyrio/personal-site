from django.contrib import admin
from mainsite.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
