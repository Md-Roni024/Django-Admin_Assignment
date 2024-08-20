from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('', views.hello, name='hello'),
    path('location/', views.location, name='location'),
    path('location/<int:location_id>/', views.get_location_by_id, name='get_location_by_id'),
    path('location/<int:location_id>/update/', views.update_location_by_id, name='update_location_by_id'),
    path('location/<int:location_id>/delete/', views.delete_location_by_id, name='delete_location_by_id'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
