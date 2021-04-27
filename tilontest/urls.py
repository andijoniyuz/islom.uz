from django.contrib import admin
from django.urls import path, include
from tilon.views import HomeView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tilon.urls')),
    path('', HomeView)
]
