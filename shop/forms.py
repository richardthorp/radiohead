import datetime
from django import forms
from .models import Album, Product
from .widgets import ItemCustomClearableFileInput


class AddAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        exclude = ('slug',)

    tracklist = forms.CharField(label="",
                                widget=forms.TextInput(
                                    attrs={'class': 'd-none'}))
    image = forms.ImageField(label='Image', required=True,
                             widget=ItemCustomClearableFileInput)
    year = forms.IntegerField(widget=forms.NumberInput(
        attrs={'min': '1985',
               'max': '2050',
               'value': datetime.date.today().year
               }))

    def __str__(self):
        return 'AddAlbumForm'


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('slug',)
    image = forms.ImageField(label='Image', required=True,
                             widget=ItemCustomClearableFileInput)

    def __str__(self):
        return 'AddProductForm'
