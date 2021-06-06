from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=128)
    release_year = models.PositiveSmallIntegerField(null=True)
    artist = models.ForeignKey(Artist, related_name='songs', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
