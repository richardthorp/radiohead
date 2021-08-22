from django.db import models
from profiles.models import Profile
from django.utils import timezone
from django.utils.text import slugify


class Single(models.Model):
    title = models.CharField(blank=False, max_length=80, unique=True)
    slug = models.SlugField(default="", max_length=80, unique=True)
    image = models.ImageField(blank=False, null=False,
                              upload_to="single_covers")
    album = models.ForeignKey('shop.Album', null=True,
                              on_delete=models.SET_NULL,
                              related_name='singles')
    video_url = models.URLField(blank=False, null=False)
    spotify_url = models.URLField(blank=False, null=False)

    def save(self, *args, **kwargs):
        if self.slug != slugify(self.title):
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

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
