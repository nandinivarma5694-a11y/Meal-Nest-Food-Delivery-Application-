from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication URLs
    path('', include('account.urls')),   # login, signup, logout, password reset, etc.
    path('customer/', include('customer.urls')), # customer dashboard, password change, etc.
    path('seller/', include('seller.urls')),     # seller dashboard

    # Food delivery app URLs
    path('', include('core.urls')),  # home, food, cart, order, etc.
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
