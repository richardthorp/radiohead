from django import forms
from .models import PortalImagesPost, PortalTextPost, PortalVideoPost
from shop.widgets import ItemCustomClearableFileInput


class AddTextPostForm(forms.ModelForm):
    class Meta:
        model = PortalTextPost
        exclude = ('slug', 'text',)
        labels = {
            'lead_image': 'Image',
            'text_content': 'Text (as HTML)'
        }
    lead_image = forms.ImageField(required=True,
                                  widget=ItemCustomClearableFileInput)

    def __str__(self):
        return 'AddTextPostForm'


class AddVideoPostForm(forms.ModelForm):
    class Meta:
        model = PortalVideoPost
        exclude = ('slug', 'video',)
    lead_image = forms.ImageField(label='Image', required=True,
                                  widget=ItemCustomClearableFileInput)

    def __str__(self):
        return 'AddVideoPostForm'


class AddImagesPostForm(forms.ModelForm):
    class Meta:
        model = PortalImagesPost
        exclude = ('slug',)
    lead_image = forms.ImageField(label='Lead Image', required=True,
                                  widget=ItemCustomClearableFileInput)
    image_1 = forms.ImageField(required=True,
                               widget=ItemCustomClearableFileInput(attrs={
                                   'name': 'image_1'
                                   }))
    image_2 = forms.ImageField(required=True,
                               widget=ItemCustomClearableFileInput)
    image_3 = forms.ImageField(widget=ItemCustomClearableFileInput,
                               required=False)
    image_4 = forms.ImageField(widget=ItemCustomClearableFileInput,
                               required=False)
    image_5 = forms.ImageField(widget=ItemCustomClearableFileInput,
                               required=False)
    image_6 = forms.ImageField(widget=ItemCustomClearableFileInput,
                               required=False)
    image_7 = forms.ImageField(widget=ItemCustomClearableFileInput,
                               required=False)
    image_8 = forms.ImageField(widget=ItemCustomClearableFileInput,
                               required=False)

    def __str__(self):
        return 'AddImagesPostForm'
