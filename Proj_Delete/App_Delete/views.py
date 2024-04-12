from django.shortcuts import render

from .djngo_delete import DjangoDelete
from .models import *


# Create your views here.
def check_delete_view(request):
    objs = Model1.objects.all().values_list('id', flat=True)
    td = DjangoDelete(Model1, objs)
    td.check_delete()
    if td.protect:
        msg = td.protect
        msg_type = 'protect'
    elif td.cascade:
        msg = td.cascade
        msg_type = 'cascade'
    else:
        msg = 'No Data'
        msg_type = 'Error'
    context = {
        'data': msg,
        'model_name': td.model_name,
        'msg_type': msg_type,
        'summary': td.summary,
    }
    return render(request, 'index.html', context)


def delete_view(request):
    objs = Model1.objects.all().values_list('id', flat=True)
    td = DjangoDelete(Model1, objs)
    td.delete()
    return render(request, 'index.html', {'msg_type': 'Success'})


def db_migration(request):
    """ Create New Records for Empty Database """
    if any([Model1.objects.all_records().exists(),
            Model2.objects.all_records().exists(),
            Model3.objects.all_records().exists(),
            Model4.objects.all_records().exists(),
            Model5.objects.all_records().exists()]):
        msg = 'Delete All Records to Apply this Migration'

    else:
        m1 = Model1.objects.create(name='1')
        m2 = Model1.objects.create(name='2')
        m3 = Model1.objects.create(name='3')
        m4 = Model1.objects.create(name='4')
        Model2.objects.create(name='21', model1_id=m1)
        m22 = Model2.objects.create(name='22', model1_id=m1)
        Model2.objects.create(name='23', model1_id=m1)
        Model3.objects.create(name='31', model1_id=m1)
        Model3.objects.create(name='32', model1_id=m1)
        Model4.objects.create(name='41', model1_id=m4)
        Model4.objects.create(name='42', model1_id=m4)
        Model4.objects.create(name='43', model1_id=m4)
        m51 = Model5.objects.create(name='51', model2_id=m22)
        m51.model1_id.add(m1, m2, m3, m4)
        Model5.objects.create(name='52', model2_id=m22)
        Model5.objects.create(name='53', model2_id=m22)
        Model5.objects.create(name='54', model2_id=m22)
        msg = 'All Records Created Successfully'
    return render(request, 'db_migration.html', {'msg': msg})

