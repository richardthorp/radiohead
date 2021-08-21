from django import forms
from .models import Profile
from .widgets import CustomClearableFileInput


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'default_email', 'portal_cust_id',
                   'subscription_id', 'subscription_status']
    image = forms.ImageField(label='Profile image', required=False,
                             widget=CustomClearableFileInput)

    default_address_line1 = forms.CharField(label='Default Address Line 1')
    default_address_line2 = forms.CharField(label='Default Address Line 2')
