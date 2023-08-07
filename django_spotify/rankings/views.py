from django.shortcuts import render
from django.http import JsonResponse
from .models import TrackRanking, ArtistsRanking

def tracks_ranking(request):
    data = list(TrackRanking.objects.values())
    return JsonResponse(data, safe=False)


def artists_ranking(request):
    data = list(ArtistsRanking.objects.values())
    return JsonResponse(data, safe=False)