from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from . import functions as sv
from .models import Channels_Ids, Channels, Servers

def index(request):
    channel = Channels.objects.all()
    server = Servers.objects.all()

    Client_Count = 0
    RPM = 0

    for data in channel:
        print(data.name, data.Client_count, data.RPM)
        Client_Count += data.Client_count
        RPM += data.RPM

    for data in list(server):
        print(data.Count, data.state)

    return render(request, 'channel/index.html', {
        'channels': channel,
        'servers': server[0],
        'Client_Count': Client_Count,
        'RPM': RPM,
    })

def get_Channel(request):
    channels = list()
    for data in Channels.objects.all():
        channels.append({
            'name': data.name,
            'Client_count': data.Client_count,
            'RPM': data.RPM
        })
    re = JsonResponse({'channels': channels})
    re['access-control-allow-origin'] = '*'
    return re

def get_Server(request):
    reJson = dict()
    for data in Servers.objects.all():
        reJson['count'] = data.Count
        reJson['state'] = data.state
    return JsonResponse(reJson)

def set_server_count(request):
    return sv.set_server()


def update_ServerState(request, state):
    serverObject = Servers.objects.all()[0]
    serverObject.state = state
    serverObject.save()

    return HttpResponse(serverObject.state)

