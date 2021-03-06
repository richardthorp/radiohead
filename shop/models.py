from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.utils import timezone


class Album(models.Model):
    title = models.CharField(blank=False, max_length=80, unique=True)
    slug = models.SlugField(default="", max_length=80, unique=True)
    year = models.IntegerField(
        blank=False, null=False, validators=[
            MinValueValidator(1985, message='The year must be at least 1985'),
            MaxValueValidator(2050, message='The year must be less than 2050')
        ])
    tracklist = models.JSONField(null=False, blank=False)
    cd_price = models.DecimalField(blank=False, null=False, max_digits=5,
                                   decimal_places=2)
    vinyl_price = models.DecimalField(blank=False, null=False, max_digits=5,
                                      decimal_places=2)
    image = models.ImageField(blank=False, null=False,
                              upload_to="album_covers")
    spotify_url = models.URLField(blank=False, null=False)
    date_added = models.DateField(blank=False, default=timezone.now)

    def save(self, *args, **kwargs):
        if self.slug != slugify(self.title):
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=80, blank=False, unique=True)
    slug = models.SlugField(default="", max_length=80, unique=True)
    category = models.TextField(choices=[('clothing', 'Clothing'),
                                         ('other', 'Other')])
    price = models.DecimalField(max_digits=5,
                                decimal_places=2)
    description = models.TextField(default="")
    has_sizes = models.BooleanField(blank=True, null=True, default=False)
    image = models.ImageField(upload_to="product_images", blank=False,
                              null=False, default='missing_item.jpg')
    date_added = models.DateField(blank=False, default=timezone.now)

    def save(self, *args, **kwargs):
        if self.slug != slugify(self.name):
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
