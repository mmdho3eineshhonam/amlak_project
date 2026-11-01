from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from properties.models import Property


class Inquiry(models.Model):
    """درخواست (استعلام) مشتری برای یک ملک و پاسخ مشاور."""

    class Status(models.TextChoices):
        NEW = "new", _("New")
        IN_PROGRESS = "in_progress", _("In progress")
        ANSWERED = "answered", _("Answered")
        CLOSED = "closed", _("Closed")

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="inquiries")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="inquiries")
    message = models.TextField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.NEW)
    agent_response = models.TextField(blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    response_email_sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Inquiry #{self.pk} · {self.property}"


class Favorite(models.Model):
    """ملکِ ذخیره‌شده توسط کاربر داخل یک لیست علاقه‌مندی."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    list = models.ForeignKey("FavoriteList", on_delete=models.CASCADE, related_name="favorites")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("user", "list", "property"), name="unique_user_favorite")]
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user} saved {self.property}"


class FavoriteList(models.Model):
    """لیست علاقه‌مندی‌های نام‌دار هر کاربر."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorite_lists")
    name = models.CharField(max_length=80)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-is_default", "name")
        constraints = [models.UniqueConstraint(fields=("user", "name"), name="unique_favorite_list_name")]

    def __str__(self):
        return self.name


class InquiryNotification(models.Model):
    """سابقه‌ی ارسال ایمیل/پیامک هنگام پاسخ به درخواست."""

    class Channel(models.TextChoices):
        EMAIL = "email", _("Email")
        SMS = "sms", _("SMS")

    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name="notifications")
    channel = models.CharField(max_length=8, choices=Channel.choices)
    sent = models.BooleanField(default=False)
    error = models.CharField(max_length=240, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.channel} notification for inquiry {self.inquiry_id}"


class ComparisonSelection(models.Model):
    """ملک‌های انتخاب‌شده توسط کاربر برای مقایسه."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comparison_selections")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="comparison_selections")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("user", "property"), name="unique_user_comparison_property")]
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.user} compares {self.property}"
