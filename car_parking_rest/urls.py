from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("cars.api.urls")),
    path('users/', include("users.api.urls")),
]
