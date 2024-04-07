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
    model1_id = models.ForeignKey('Model1', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Model3(MyModel):
    name = models.CharField(max_length=100)
    model2_id = models.ManyToManyField('Model2', blank=True)

    def __str__(self):
        return self.name


class Model4(MyModel):
    name = models.CharField(max_length=100)
    model3_id = models.ManyToManyField('Model3', blank=True)
    model3_id2 = models.ForeignKey('Model3', on_delete=models.CASCADE, related_name='model4s_by_fk', null=True, blank=True)

    def __str__(self):
        return self.name


class Model5(MyModel):
    name = models.CharField(max_length=100)
    model4_id = models.ForeignKey('Model4', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.name


class Model6(MyModel):
    model5_id = models.OneToOneField('Model5', on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Model7(MyModel):
    model6_id = models.OneToOneField('Model6', on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


