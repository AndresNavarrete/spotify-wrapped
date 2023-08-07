from django.http import JsonResponse
from django.shortcuts import render

from .models import ArtistsRanking, TrackRanking


def tracks_ranking(request):
    data = list(TrackRanking.objects.values())
    return JsonResponse(data, safe=False)


def artists_ranking(request):
    data = list(ArtistsRanking.objects.values())
    return JsonResponse(data, safe=False)
