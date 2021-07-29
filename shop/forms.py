# from django.forms import ModelForm
from django import forms
from .models import Album, Product


class AddAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = '__all__'

    tracklist = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'class': 'd-none'})
        )

    def __str__(self):
        return 'AddAlbumForm'


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __str__(self):
        return 'AddProductForm'
