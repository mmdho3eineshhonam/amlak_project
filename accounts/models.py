import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """کاربر سایت؛ نقش (مشتری / مشاور املاک) با فیلد role مشخص می‌شود."""

    class Role(models.TextChoices):
        CUSTOMER = "customer", _("Customer")
        AGENT = "agent", _("Real estate agent")

    role = models.CharField(max_length=16, choices=Role.choices, default=Role.CUSTOMER)
    phone_number = models.CharField(max_length=24, blank=True)
    email_verified = models.BooleanField(default=False)
    sms_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name() or self.username


class EmailVerification(models.Model):
    """توکن تأیید ایمیل کاربر."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="email_verifications")
    token = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(default=timezone.now)
    used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Email verification for {self.user}"


class SMSVerification(models.Model):
    """کد تأیید پیامکی کاربر (به‌صورت هش‌شده)."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="sms_verification")
    code_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(default=timezone.now)
    attempts = models.PositiveSmallIntegerField(default=0)
    last_sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"SMS verification for {self.user}"
