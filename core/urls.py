from django.contrib import admin
from django.urls import path, include
from accounts import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.user_home, name="home"),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('destinations/', include('destinations.urls')),
    path('reviews/', include('reviews.urls')),
    path('enquiries/', include('enquiries.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('chat/', include('chat_support.urls')),
    path('trip/', include('trips.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )