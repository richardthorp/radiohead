# from django.forms import ModelForm
from django import forms
from .models import Album, Product
import datetime


class AddAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = '__all__'

    tracklist = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'd-none'})
        )
    year = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': '1985',
                                        'max': '2050',
                                        'value': datetime.date.today().year
                                        })
        )

    def __str__(self):
        return 'AddAlbumForm'


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __str__(self):
        return 'AddProductForm'
