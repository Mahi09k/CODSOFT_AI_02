from django.contrib import admin
from django.urls import path, include   # Include for including app URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('game.urls')),  # Include app-specific URLs from game app
]
