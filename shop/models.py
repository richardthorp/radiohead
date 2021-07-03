from django.db import models


class Album(models.Model):
    title = models.CharField(blank=False, max_length=80)
    year = models.IntegerField(blank=False, null=False)
    tracklist = models.JSONField(null=False, blank=False)
    cd_price = models.DecimalField(blank=False, null=False, max_digits=5,
                                   decimal_places=2)
    vinyl_price = models.DecimalField(blank=False, null=False, max_digits=5,
                                      decimal_places=2)
    image = models.ImageField(blank=False,
                              null=False)
    spotify_url = models.URLField(blank=False, null=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=80)
    category = models.TextField(choices=[('clothing', 'Clothing'),
                                         ('other', 'Other')])
    price = models.DecimalField(max_digits=5,
                                decimal_places=2)
    description = models.TextField(default="")
    has_sizes = models.BooleanField(blank=True, null=True, default=False)
    image = models.ImageField(upload_to="product_images", blank=False,
                              null=False, default='missing_item.jpg')

    def __str__(self):
        return self.name
