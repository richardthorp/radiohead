from django.forms import ModelForm
from .models import Album, Product


class AddAlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = '__all__'

    def __str__(self):
        return 'AddAlbumForm'


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __str__(self):
        return 'AddProductForm'
