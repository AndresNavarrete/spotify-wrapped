from django.db import models


class ArtistsRanking(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    image_url = models.URLField()
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = "public.artists_time_in_top"


class TrackRanking(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    image_url = models.URLField()
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = "public.tracks_time_in_top"
