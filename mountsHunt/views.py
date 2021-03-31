import json
import os

from django.shortcuts import render
from django.http import HttpResponse
from .models import Mount

def Hello(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    mount_list = Mount.objects.all()
    context = {'mount_list': mount_list}
    return render(request, 'mountsHunt/index.html', context)

def load_mounts_form_json(request):
    #file = open('./anotherapp/baz.txt')
    path = os.getcwd() + '/mountsHunt/data/'
    file_list = os.listdir(path)
    for f in file_list:
        with open(path + f, encoding='utf-8') as data_file:
            json_data = json.loads(data_file.read())

            for mount_data in json_data:
                mount = Mount.create(**mount_data)
    return HttpResponse("All good.")
