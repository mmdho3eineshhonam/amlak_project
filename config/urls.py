from django.contrib import admin
from django.urls import path

# فاز اول: فقط پنل ادمین برای مشاهده‌ی مدل‌ها. URLهای سایت در فاز دوم تعریف می‌شوند.
urlpatterns = [
    path("admin/", admin.site.urls),
]
