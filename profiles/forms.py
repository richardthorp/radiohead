from django import forms
from .models import Profile
from .widgets import ProfileCustomClearableFileInput


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'default_email', 'portal_cust_id',
                   'subscription_id', 'subscription_status']
    image = forms.ImageField(label='', required=False,
                             widget=ProfileCustomClearableFileInput)

    default_address_line1 = forms.CharField(label='Default Address Line 1',
                                            required=False)
    default_address_line2 = forms.CharField(label='Default Address Line 2',
                                            required=False)
