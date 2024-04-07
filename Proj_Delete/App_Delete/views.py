from django.shortcuts import render

from .djngo_delete import DjangoDelete
from .models import *


# Create your views here.
def check_delete_view(request):
    objs = Model5.objects.all().values_list('id', flat=True)
    td = DjangoDelete(Model5, objs)
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
    objs = Model5.objects.all().values_list('id', flat=True)
    td = DjangoDelete(Model5, objs)
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


