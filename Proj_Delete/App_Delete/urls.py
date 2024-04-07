from django.urls import path
from . import views


urlpatterns = [
    path('', views.delete_view, name='delete'),
    path('check_delete', views.check_delete_view, name='check_delete'),
]
