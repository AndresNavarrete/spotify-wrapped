from django.db import models


class ArtistsRanking(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    image_url = models.URLField()
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = "artists_time_in_top"


class TrackRanking(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    image_url = models.URLField()
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = "tracks_time_in_top"
