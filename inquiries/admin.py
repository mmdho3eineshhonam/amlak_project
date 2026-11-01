from django.contrib import admin
from .models import ComparisonSelection, Favorite, FavoriteList, Inquiry, InquiryNotification


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "customer", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("property__title", "customer__username", "message")


admin.site.register(Favorite)
admin.site.register(FavoriteList)
admin.site.register(ComparisonSelection)
admin.site.register(InquiryNotification)
