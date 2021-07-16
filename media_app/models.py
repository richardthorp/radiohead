from django.db import models
# from django.contrib.auth.models import User
from profiles.models import Profile
from django.utils import timezone


class Single(models.Model):
    title = models.TextField(blank=False)
    image = models.ImageField(blank=False, null=False,
                              upload_to="single_covers")
    album = models.ForeignKey('shop.Album', null=True,
                              on_delete=models.SET_NULL)
    video_url = models.URLField(blank=False, null=False)
    spotify_url = models.URLField(blank=False, null=False)
    # comments = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(blank=False)
    posted_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    on_single = models.ForeignKey(Single, on_delete=models.CASCADE)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.posted_by} on {self.date_posted}.'
