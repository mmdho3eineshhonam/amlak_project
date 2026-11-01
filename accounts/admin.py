from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import EmailVerification, SMSVerification, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (("Profile", {"fields": ("role", "phone_number", "email_verified", "sms_verified")}),)
    list_display = ("username", "email", "role", "is_active", "email_verified", "sms_verified")
    list_filter = ("role", "is_active", "email_verified", "sms_verified")


admin.site.register(EmailVerification)
admin.site.register(SMSVerification)
