from django.forms import ModelForm
from .models import Album, Product


class AddAlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = '__all__'


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
