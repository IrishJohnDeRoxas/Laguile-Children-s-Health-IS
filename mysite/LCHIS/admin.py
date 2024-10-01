# from django.contrib import admin
# from .models import Child, Guardian

# class ChildInline(admin.StackedInline):
#     model = Guardian

# class GuardianAdmin(admin.ModelAdmin):
#     inlines = [ChildInline]

# admin.site.register(Child, GuardianAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import GuardianModel

admin.site.register(GuardianModel, UserAdmin)
