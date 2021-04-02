import os
import json

from django.conf import settings
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from mountsHunt.models import Mount

def Hello(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def index_old(request):
    mount_list = Mount.objects.all()
    context = {'mount_list': mount_list}
    return render(request, 'mountsHunt/index.html', context)

#################################
# VUE
#################################
def index(request):
    return render(request, 'mountsHunt/index.html')

# @csrf_exempt
@require_http_methods(["GET"])
def allMounts(request):
    try:
        mounts = Mount.objects.all()
    except Mount.DoesNotExist:
        mounts = []
    data = []
    for m in mounts:
        mount = { 
            "id": m.id,
            "name": m.name,
            # "expansion": m.expansion,
            # "notes_1": m.notes_1,
            # "notes_2": m.notes_2,
            # "requirements": m.requirements,
            # "source": m.source,
            # "url_info": m.url_info,
            # "url_wowhead": m.url_wowhead,
            "image_mini": m.image_mini,
            # "image": m.image,
            # "url_img": m.url_img,
            "url_img_min": m.url_img_min
        }
        data.append(mount)
    return HttpResponse(json.dumps(data), content_type="application/json")

@require_http_methods(["GET"])
def getMount(request, pk):
    try:
        m = Mount.objects.filter(pk=pk).first()
    except Mount.DoesNotExist:
        m = None
    data = {
        "id": m.id,
        "name": m.name,
        "expansion": m.expansion,
        "notes_1": m.notes_1,
        "notes_2": m.notes_2,
        "requirements": m.requirements,
        "source": m.source,
        "url_info": m.url_info,
        "url_wowhead": m.url_wowhead,
        "image_mini": m.image_mini,
        "image": m.image,
        "url_img": m.url_img,
        "url_img_min": m.url_img_min
    }
    return HttpResponse(json.dumps(data), content_type="application/json")

#################################
# EXTRA
#################################
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