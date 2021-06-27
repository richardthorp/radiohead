from django.db import models


class Album(models.Model):
    name = models.TextField(blank=False)
    year = models.IntegerField(blank=False, null=False)
    tracklist = models.JSONField(null=False, blank=False)
    cd_price = models.DecimalField(blank=False, null=False, max_digits=5,
                                   decimal_places=2)
    vinyl_price = models.DecimalField(blank=False, null=False, max_digits=5,
                                      decimal_places=2)
    image = models.ImageField(upload_to='album_covers/', blank=False,
                              null=False)
    spotify_url = models.URLField(blank=False, null=False)

    def __str__(self):
        return self.name
