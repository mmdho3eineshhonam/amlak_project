from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Amenity(models.Model):
    """امکانات ملک (پارکینگ، آسانسور، ...)."""

    name = models.CharField(max_length=80, unique=True)
    icon = models.CharField(max_length=40, blank=True, help_text="Optional icon name used by the UI.")

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "amenities"

    def __str__(self):
        return self.name


class Property(models.Model):
    """آگهی ملک که توسط مشاور املاک (owner) ثبت می‌شود."""

    class PropertyType(models.TextChoices):
        APARTMENT = "apartment", _("Apartment")
        HOUSE = "house", _("House")
        VILLA = "villa", _("Villa")
        LAND = "land", _("Land")

    class DealType(models.TextChoices):
        SALE = "sale", _("For sale")
        RENT = "rent", _("For rent")

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="properties")
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    property_type = models.CharField(max_length=16, choices=PropertyType.choices)
    deal_type = models.CharField(max_length=8, choices=DealType.choices)
    city = models.CharField(max_length=80)
    neighborhood = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    area_sqm = models.PositiveIntegerField()
    price = models.PositiveBigIntegerField(help_text="Sale price or monthly rent, in the local currency.")
    deposit = models.PositiveBigIntegerField(default=0, blank=True)
    bedrooms = models.PositiveSmallIntegerField(default=0)
    bathrooms = models.PositiveSmallIntegerField(default=1)
    built_year = models.PositiveSmallIntegerField(null=True, blank=True)
    cover_image = models.URLField(blank=True)
    amenities = models.ManyToManyField(Amenity, blank=True, related_name="properties")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [models.Index(fields=("city", "deal_type", "is_published"))]

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    """تصاویر بارگذاری‌شده برای یک ملک."""

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="properties/%Y/%m/")
    alt_text = models.CharField(max_length=180, blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("position", "id")

    def __str__(self):
        return f"Image for {self.property}"


class PropertyView(models.Model):
    """ثبت هر بازدید از صفحه‌ی یک ملک."""

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="views")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=("property", "viewed_at"))]

    def __str__(self):
        return f"View of {self.property}"
