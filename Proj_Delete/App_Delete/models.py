from django.db import models


# Create your models here.
class AdminManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Manager(models.Manager):
    def all_records(self):
        return super().get_queryset()

    def get_queryset(self):
        return super().get_queryset().filter(is_del=False)


class MyModel(models.Model):
    admin_objects = AdminManager()
    objects = Manager()
    is_del = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Model1(MyModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Model2(MyModel):
    name = models.CharField(max_length=100)
    model1_id = models.ForeignKey('Model1', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Model3(MyModel):
    name = models.CharField(max_length=100)
    model1_id = models.ForeignKey('Model1', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Model4(MyModel):
    name = models.CharField(max_length=100)
    model1_id = models.ForeignKey('Model1', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Model5(MyModel):
    name = models.CharField(max_length=100)
    model1_id = models.ManyToManyField('Model1', blank=True)
    model2_id = models.ForeignKey('Model2', on_delete=models.CASCADE)

    def __str__(self):
        return self.name










