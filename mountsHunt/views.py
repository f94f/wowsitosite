import os
import json
import sys

from django.db import connection
from django.conf import settings
from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from types import SimpleNamespace

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

@require_http_methods(["GET"])
def firstLoad(request):
    mounts = []
    expansions = []
    types = []
    factions = []
    zones = []
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT M.ID, M.Name, M.Image_mini, M.Image, M.URL_img, M.URL_img_min FROM MOUNT M ORDER BY M.Name")
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            mounts.append(dict(zip(columns, row)))
        
        cursor.execute("SELECT E.ID, E.Name FROM EXPANSION E ORDER BY E.ID")
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            expansions.append(dict(zip(columns, row)))
        
        cursor.execute("SELECT TM.ID, TM.Name FROM TYPE_MOUNT TM ORDER BY TM.ID")
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            types.append(dict(zip(columns, row)))
        
        cursor.execute("SELECT F.ID, F.Name FROM FACTION F ORDER BY F.ID")
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            factions.append(dict(zip(columns, row)))
        
        cursor.execute("SELECT Z.ID, Z.Name FROM ZONE Z ORDER BY Z.ID")
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            zones.append(dict(zip(columns, row)))
    except:
        mounts = []
    
    data = { 'mounts': mounts, 'expansions': expansions, 'types': types, 'factions': factions, 'zones': zones }
    return HttpResponse(json.dumps(data), content_type="application/json")

@require_http_methods(["GET"])
def allMounts(request):
    data = []
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT M.ID, M.Name, M.Image_mini, M.Image, M.URL_img, M.URL_img_min FROM MOUNT M ORDER BY M.Name")
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            data.append(dict(zip(columns, row)))
    except:
        data = []
    return HttpResponse(json.dumps(data), content_type="application/json")

@require_http_methods(["GET"])
def getMount(request, pk):
    data = None
    try:
        print(pk)
        cursor = connection.cursor()
        cursor.execute("SELECT M.ID , M.Name, E.Name Expansion, M.Notes_1, M.Notes_2, M.Requirements, M.Source, "
                    "Z.Name Zone, M.URL_info, M.URL_wowhead, M.Image_mini, M.Image, M.URL_img, M.URL_img_min, "
                    "F.Name Faction, TM.Name Type, TT.Name Type_Timing "
                    "FROM MOUNT M "
                    "LEFT OUTER JOIN EXPANSION E ON M.Expansion_id = E.ID "
                    "LEFT OUTER JOIN FACTION F ON M.Faction_id = F.ID "
                    "LEFT OUTER JOIN TYPE_MOUNT TM ON M.Type_id = TM.ID "
                    "LEFT OUTER JOIN TYPE_TIMING TT ON M.Type_timing_id = TT.ID "
                    "LEFT OUTER JOIN ZONE Z ON M.Zone_id = Z.ID "
                    "WHERE M.ID = %s", [pk])
        columns = [column[0] for column in cursor.description]
        data = dict(zip(columns, cursor.fetchone()))
    except:
        print(sys.exc_info())
        data = None
    return HttpResponse(json.dumps(data), content_type="application/json")

@csrf_exempt
@require_http_methods(["POST"])
def filterMounts(request):
    print(request.body)
    filter = json.loads(str(request.body, encoding='utf-8'))["filter"]
    print(filter)
    data = []
    try:
        query = "SELECT M.ID, M.Name, M.Image_mini, M.Image, M.URL_img, M.URL_img_min \
        FROM MOUNT M \
        LEFT OUTER JOIN EXPANSION E ON M.Expansion_id = E.ID \
        LEFT OUTER JOIN FACTION F ON M.Faction_id = F.ID \
        LEFT OUTER JOIN TYPE_MOUNT TM ON M.Type_id = TM.ID \
        LEFT OUTER JOIN TYPE_TIMING TT ON M.Type_timing_id = TT.ID \
        LEFT OUTER JOIN ZONE Z ON M.Zone_id = Z.ID "

        params = []
        # NAME
        if not filter["name"]:
            query = query + "WHERE M.Name LIKE %s "
            params.append("%")
        else:
            query = query + "WHERE M.Name LIKE %s "
            params.append("%" + filter["name"] + "%")
        
        # EXPANSIONE
        if len(filter["expansions"]) == 0 or "0" in filter["expansions"]:
            query = query + "AND (E.ID LIKE %s OR E.ID IS NULL) "
            params.append("%")
        else:
            count = 0
            query = query + "AND (E.ID IN ("
            for e in filter["expansions"]:
                count = count + 1
                query = query + " %s "
                if len(filter["expansions"]) > 1 and count < len(filter["expansions"]):
                    query = query + ","
                params.append(e)
            query = query + ") OR E.ID IS NULL) "

        # TYPE
        if len(filter["type"]) == 0 or "all" in filter["type"]:
            query = query + "AND (TM.ID LIKE %s OR TM.ID IS NULL) "
            params.append("%")
        else:
            count = 0
            query = query + "AND TM.ID IN ("
            for e in filter["type"]:
                count = count + 1
                query = query + " %s "
                if len(filter["type"]) > 1 and count < len(filter["type"]):
                    query = query + ","
                params.append(e)
            query = query + ") "

        # FACTION
        if filter["faction"] == 1:
            query = query + "AND (F.ID LIKE %s OR F.ID IS NULL) "
            params.append("%")
        else:
            query = query + "AND F.ID = %s "
            params.append(filter["faction"])
        
        # ZONE
        if len(filter["zone"]) == 0 or "all" in filter["zone"]:
            query = query + "AND (Z.ID LIKE %s OR Z.ID IS NULL) "
            params.append("%")
        else:
            count = 0
            query = query + "AND Z.ID IN ("
            for e in filter["zone"]:
                count = count + 1
                query = query + " %s "
                if len(filter["zone"]) > 1 and count < len(filter["zone"]):
                    query = query + ","
                params.append(e)
            query = query + ") "

        query = query + "ORDER BY M.Name"
        print(query)
        print(params)

        cursor = connection.cursor()
        cursor.execute(query, params)
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            data.append(dict(zip(columns, row)))
    except:
        print(sys.exc_info())
        data = None
    
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

    cursor = connection.cursor()
    cursor.execute("DELETE FROM MOUNT")
    for f in file_list:
        with open(path + f, encoding='utf-8') as data_file:
            json_data = json.loads(data_file.read())

            for mount_data in json_data:
                URL_img = mount_data["Id"] + "-" + mount_data["Name"].replace('/', ' ') + "/" + mount_data["Image"]
                URL_img_min = mount_data["Id"] + "-" + mount_data["Name"].replace('/', ' ') + "/" + mount_data["ImageMini"]
                params = [mount_data["Id"], mount_data["Name"], get_dict_expansion(mount_data["Expansion"]), mount_data["Notes_1"], mount_data["Notes_2"],
                     mount_data["Requirements"], mount_data["Source"], None, mount_data["UrlInfo"], mount_data["UrlWowhead"], mount_data["ImageMini"],
                     mount_data["Image"], URL_img, URL_img_min, None, None, None]
                cursor.execute("INSERT INTO MOUNT (ID,Name,Expansion_id,Notes_1,Notes_2,Requirements,Source,Zone_id,"
                    "URL_info,URL_wowhead,Image_mini,Image,URL_img,URL_img_min,Faction_id,Type_id,Type_timing_id) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", params)
    return HttpResponse("All good.")

def get_dict_expansion(expansion):
    try:
        thisdict =	{
            "Original": "1",
            "The Burning Crusade": "2",
            "Wrath of The Lich King": "3",
            "Cataclysm": "4",
            "Mist of Pandaria": "5",
            "Warlords of Draenor": "6",
            "Legion": "7",
            "Battle for Azeroth": "8",
            "Shadowlands": "9"
        }
        return thisdict[expansion]
    except:
        return "0"
