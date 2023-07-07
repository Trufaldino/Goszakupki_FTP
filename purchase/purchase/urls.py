from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    # Other URL patterns
    path('', include('purchase_app.urls')),
]
