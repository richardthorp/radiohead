from django import forms
from shop.widgets import GeneralCustomClearableFileInput
from .models import PortalImagesPost, PortalTextPost, PortalVideoPost
from .widgets import ImagesPostCustomClearableFileInput


class AddTextPostForm(forms.ModelForm):
    class Meta:
        model = PortalTextPost
        exclude = ('slug', 'text',)
        labels = {
            'text_content': 'Text (as HTML)'
        }
    lead_image = forms.ImageField(required=True, label="",
                                  widget=GeneralCustomClearableFileInput)

    def __str__(self):
        return 'AddTextPostForm'


class AddVideoPostForm(forms.ModelForm):
    class Meta:
        model = PortalVideoPost
        exclude = ('slug', 'video',)
    lead_image = forms.ImageField(required=True, label='',
                                  widget=GeneralCustomClearableFileInput)

    def __str__(self):
        return 'AddVideoPostForm'


class AddImagesPostForm(forms.ModelForm):
    class Meta:
        model = PortalImagesPost
        exclude = ('slug',)
    lead_image = forms.ImageField(required=True, label='',
                                  widget=GeneralCustomClearableFileInput)
    image_1 = forms.ImageField(required=True, label='',
                               widget=ImagesPostCustomClearableFileInput)
    image_2 = forms.ImageField(required=True, label='',
                               widget=ImagesPostCustomClearableFileInput)
    image_3 = forms.ImageField(required=False, label='',
                               widget=ImagesPostCustomClearableFileInput)
    image_4 = forms.ImageField(required=False, label='',
                               widget=ImagesPostCustomClearableFileInput)
    image_5 = forms.ImageField(required=False, label='',
                               widget=ImagesPostCustomClearableFileInput)
    image_6 = forms.ImageField(required=False, label='',
                               widget=ImagesPostCustomClearableFileInput)
    image_7 = forms.ImageField(required=False, label='',
                               widget=ImagesPostCustomClearableFileInput)
    image_8 = forms.ImageField(required=False, label='',
                               widget=ImagesPostCustomClearableFileInput)

    def __str__(self):
        return 'AddImagesPostForm'
