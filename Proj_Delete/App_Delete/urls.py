from django.urls import path
from . import views


urlpatterns = [
    path('confirm_delete/', views.delete_view, name='delete'),
    path('check_delete', views.check_delete_view, name='check_delete'),
    path('db_migration', views.db_migration, name='db_migration'),
]








