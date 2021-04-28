from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tilon.urls'))
]

handler404 = 'apis.views.page_not_found'
handler500 = 'apis.views.handler500'
