from django.db import models
from django.utils import timezone


class PortalTextPost(models.Model):
    title = models.CharField(blank=False, max_length=80)
    lead_image = models.ImageField(blank=False, null=False,
                                   upload_to="portal_images")
    lead_image_summary = models.CharField(blank=False, max_length=60)
    text_content = models.TextField(blank=False)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Text post: {self.title}"


class PortalVideoPost(models.Model):
    title = models.CharField(blank=False, max_length=80)
    lead_image = models.ImageField(blank=False, null=False,
                                   upload_to="portal_images")
    lead_image_summary = models.CharField(blank=False, max_length=60)
    video_url = models.URLField(blank=False, null=False)
    text_content = models.TextField(blank=False)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Video post: {self.title}"


class PortalImagesPost(models.Model):
    title = models.CharField(blank=False, max_length=80)
    lead_image = models.ImageField(blank=False, null=False,
                                   upload_to="portal_images")
    lead_image_summary = models.CharField(blank=False, max_length=60)
    post_text_content = models.TextField(blank=False)
    image_1 = models.ImageField(blank=False, null=False,
                                upload_to="portal_images")
    image_1_summary = models.CharField(blank=False, max_length=60)
    image_2 = models.ImageField(blank=False, null=False,
                                upload_to="portal_images")
    image_2_summary = models.CharField(blank=False, max_length=60)
    image_3 = models.ImageField(blank=True, null=True,
                                upload_to="portal_images")
    image_3_summary = models.CharField(blank=True, max_length=60)
    image_4 = models.ImageField(blank=True, null=True,
                                upload_to="portal_images")
    image_4_summary = models.CharField(blank=True, max_length=60)
    image_5 = models.ImageField(blank=True, null=True,
                                upload_to="portal_images")
    image_5_summary = models.CharField(blank=True, max_length=60)
    image_6 = models.ImageField(blank=True, null=True,
                                upload_to="portal_images")
    image_6_summary = models.CharField(blank=True, max_length=60)
    image_7 = models.ImageField(blank=True, null=True,
                                upload_to="portal_images")
    image_7_summary = models.CharField(blank=True, max_length=60)
    image_8 = models.ImageField(blank=True, null=True,
                                upload_to="portal_images")
    image_8_summary = models.CharField(blank=True, max_length=60)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Images post: {self.post_title}"
