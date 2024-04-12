from django.contrib import admin

from .models import *


# Register your models here.
@admin.action()
def undo_delete(modeladmin, request, queryset):
    queryset.update(is_del=False)


class Admin(admin.ModelAdmin):
    actions = [undo_delete]


@admin.register(Model1)
class Model1Admin(Admin):
    list_display = ['id', 'is_del', 'name']


@admin.register(Model2)
class Model2Admin(Admin):
    list_display = ['id', 'is_del', 'name', 'model1_id']


@admin.register(Model3)
class Model3Admin(Admin):
    list_display = ['id', 'is_del', 'name', 'model1_id']


@admin.register(Model4)
class Model4Admin(Admin):
    list_display = ['id', 'is_del', 'name', 'model1_id']


@admin.register(Model5)
class Model5Admin(Admin):
    list_display = ['id', 'is_del', 'name', 'model2_id', 'model1_ids']

    @staticmethod
    def model1_ids(obj):
        return ", ".join([str(item) for item in obj.model1_id.all()])







