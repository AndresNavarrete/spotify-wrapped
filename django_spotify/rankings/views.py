from django.http import JsonResponse
from django.shortcuts import render

from .models import (
    ArtistsRanking,
    ArtistsRankingDetails,
    TrackRanking,
    TracksRankingDetails,
)


def tracks_ranking(request):
    data = list(TrackRanking.objects.values())
    return JsonResponse(data, safe=False)


def artists_ranking(request):
    data = list(ArtistsRanking.objects.values())
    return JsonResponse(data, safe=False)


def artists_ranking_details(request):
    data = list(ArtistsRankingDetails.objects.values())
    return JsonResponse(data, safe=False)


def tracks_ranking_details(request):
    data = list(TracksRankingDetails.objects.values())
    return JsonResponse(data, safe=False)
