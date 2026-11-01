from django.contrib import admin
from .models import Amenity, Property, PropertyImage, PropertyView


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 0


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "city", "deal_type", "price", "is_published")
    list_filter = ("deal_type", "property_type", "city", "is_published")
    search_fields = ("title", "city", "neighborhood", "address")
    prepopulated_fields = {"slug": ("title",)}
    inlines = (PropertyImageInline,)


admin.site.register(Amenity)
admin.site.register(PropertyView)
