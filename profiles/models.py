from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="profile_pics",
                              default='profile_pics/default_profile_pic.jpg')
    default_name = models.CharField(max_length=150, blank=True)
    default_email = models.EmailField(max_length=256, blank=True)
    default_phone_number = models.CharField(max_length=20, blank=True)
    default_address_line1 = models.CharField(max_length=80, blank=True)
    default_address_line2 = models.CharField(max_length=80, blank=True)
    default_town_or_city = models.CharField(max_length=40, blank=True)
    default_county = models.CharField(max_length=80, blank=True)
    default_postcode = models.CharField(max_length=20, blank=True)
    default_country = CountryField(blank_label='Select Country', blank=True)
    portal_cust_id = models.CharField(max_length=256, blank=True)
    subscription_id = models.CharField(max_length=256, blank=True)
    subscription_status = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
