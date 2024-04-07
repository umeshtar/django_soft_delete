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
    list_display = ['id', 'is_del', 'name', 'model2_ids']

    @staticmethod
    def model2_ids(obj):
        return ', '.join([str(row) for row in obj.model2_id.all()])


@admin.register(Model4)
class Model4Admin(Admin):
    list_display = ['id', 'is_del', 'name', 'model3_ids', 'model3_id2']

    @staticmethod
    def model3_ids(obj):
        return ', '.join([str(row) for row in obj.model3_id.all()])


@admin.register(Model5)
class Model5Admin(Admin):
    list_display = ['id', 'is_del', 'name', 'model4_id']


@admin.register(Model6)
class Model6Admin(Admin):
    list_display = ['model5_id', 'is_del', 'name']


@admin.register(Model7)
class Model7Admin(Admin):
    list_display = ['model6_id', 'is_del', 'name']






