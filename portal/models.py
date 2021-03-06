from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from profiles.models import Profile


class PortalTextPost(models.Model):
    title = models.CharField(blank=False, max_length=80, unique=True)
    post_blurb = models.CharField(blank=False, max_length=250)
    slug = models.SlugField(default="", max_length=80, unique=True)
    lead_image = models.ImageField(blank=False, null=False,
                                   upload_to="portal_images")
    lead_image_summary = models.CharField(blank=False, max_length=200)
    text_content = models.TextField(blank=False)
    date_posted = models.DateTimeField(default=timezone.now)
    text = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return f"Text post: {self.title}"

    def save(self, *args, **kwargs):
        if self.slug != slugify(self.title):
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)


class TextPostComment(models.Model):
    text = models.TextField(blank=False)
    posted_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(PortalTextPost, on_delete=models.CASCADE)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.posted_by} on {self.date_posted}.'


class PortalVideoPost(models.Model):
    title = models.CharField(blank=False, max_length=80, unique=True)
    post_blurb = models.CharField(blank=False, max_length=250)
    slug = models.SlugField(default="", max_length=80, unique=True)
    lead_image = models.ImageField(blank=False, null=False,
                                   upload_to="portal_images")
    lead_image_summary = models.CharField(blank=False, max_length=200)
    video_url = models.URLField(blank=False, null=False)
    text_content = models.TextField(blank=False)
    date_posted = models.DateTimeField(default=timezone.now)
    video = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return f"Video post: {self.title}"

    def save(self, *args, **kwargs):
        if self.slug != slugify(self.title):
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)


class VideoPostComment(models.Model):
    text = models.TextField(blank=False)
    posted_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(PortalVideoPost, on_delete=models.CASCADE)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.posted_by} on {self.date_posted}.'


class PortalImagesPost(models.Model):
    title = models.CharField(blank=False, max_length=80, unique=True)
    post_blurb = models.CharField(blank=False, max_length=250)
    slug = models.SlugField(default="", max_length=80, unique=True)
    lead_image = models.ImageField(blank=False, null=False,
                                   upload_to="portal_images")
    lead_image_summary = models.CharField(blank=False, max_length=200)
    text_content = models.TextField(blank=False)
    image_1 = models.ImageField(blank=False, null=False,
                                upload_to="portal_images")
    image_1_summary = models.CharField(blank=False, max_length=200)
    image_2 = models.ImageField(blank=False, null=False,
                                upload_to="portal_images")
    image_2_summary = models.CharField(blank=False, max_length=200)
    image_3 = models.ImageField(blank=True, null=True,
                                upload_to="portal_images")
    image_3_summary = models.CharField(blank=True, max_length=200)
    image_4 = models.ImageField(blank=True, null=True,
                                upload_to="portal_images")
    image_4_summary = models.CharField(blank=True, max_length=200)
    image_5 = models.ImageField(blank=True, null=True,
                                upload_to="portal_images")
    image_5_summary = models.CharField(blank=True, max_length=200)
    image_6 = models.ImageField(blank=True, null=True,
                                upload_to="portal_images")
    image_6_summary = models.CharField(blank=True, max_length=200)
    image_7 = models.ImageField(blank=True, null=True,
                                upload_to="portal_images")
    image_7_summary = models.CharField(blank=True, max_length=200)
    image_8 = models.ImageField(blank=True, null=True,
                                upload_to="portal_images")
    image_8_summary = models.CharField(blank=True, max_length=200)
    date_posted = models.DateTimeField(default=timezone.now)
    images = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return f"Images post: {self.title}"

    def save(self, *args, **kwargs):
        if self.slug != slugify(self.title):
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)


class ImagesPostComment(models.Model):
    text = models.TextField(blank=False)
    posted_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(PortalImagesPost,
                             on_delete=models.CASCADE)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.posted_by} on {self.date_posted}.'
