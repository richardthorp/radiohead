from django.db import models


class Single(models.Model):
    title = models.TextField(blank=False)
    image = models.ImageField(blank=False, null=False)
    album = models.ForeignKey('shop.Album', null=True,
                              on_delete=models.SET_NULL)
    video_url = models.URLField(blank=False, null=False)
    spotify_url = models.URLField(blank=False, null=False)

    def __str__(self):
        return self.title
