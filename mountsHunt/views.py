import os
import json

from django.conf import settings
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse
from mountsHunt.models import Mount

def Hello(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    mount_list = Mount.objects.all()
    context = {'mount_list': mount_list}
    return render(request, 'mountsHunt/index.html', context)

def getMount(request, pk):
    try:
        mount = Mount.objects.filter(pk=pk).first()
    except Mount.DoesNotExist:
        mount = None
    print(mount)
    data = serialize("json", [mount], fields=('title', 'content'))
    return HttpResponse(data, content_type="application/json")

def img(request, pk, tipo):
    try:
        mount = Mount.objects.filter(pk=pk).first()
    except Mount.DoesNotExist:
        return HttpResponse(status=404)
    
    ext = mount.name.split('.')[1]
    path = "mountsHunt/img/" + mount.url_img

    file_data = None
    if tipo == "mini":
        file_data = open(os.path.join(os.getcwd(), path), "rb").read()
    else:
        file_data = open(os.path.join(os.getcwd(), path), "rb").read()

    return HttpResponse(file_data, content_type=ext)

def load_mounts_form_json(request):
    path = os.getcwd() + '/mountsHunt/data/'
    file_list = os.listdir(path)
    for f in file_list:
        with open(path + f, encoding='utf-8') as data_file:
            json_data = json.loads(data_file.read())

            for mount_data in json_data:
                mount = Mount.create(**mount_data)
    return HttpResponse("All good.")
