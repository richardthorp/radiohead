from django import forms
from .models import PortalImagesPost, PortalTextPost, PortalVideoPost
from profiles.widgets import CustomClearableFileInput


class AddTextPostForm(forms.ModelForm):
    class Meta:
        model = PortalTextPost
        exclude = ('slug', 'text',)
    lead_image = forms.ImageField(label='Image', required=True,
                                  widget=CustomClearableFileInput)

    def __str__(self):
        return 'AddTextPostForm'


class AddVideoPostForm(forms.ModelForm):
    class Meta:
        model = PortalVideoPost
        exclude = ('slug', 'video',)
    lead_image = forms.ImageField(label='Image', required=True,
                                  widget=CustomClearableFileInput)

    def __str__(self):
        return 'AddVideoPostForm'


class AddImagesPostForm(forms.ModelForm):
    class Meta:
        model = PortalImagesPost
        exclude = ('slug',)
    lead_image = forms.ImageField(label='Image', required=True,
                                  widget=CustomClearableFileInput)

    def __str__(self):
        return 'AddImagesPostForm'
