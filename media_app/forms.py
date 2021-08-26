from django import forms
from .models import Comment, Single
from shop.widgets import ItemCustomClearableFileInput


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class AddSingleForm(forms.ModelForm):
    class Meta:
        model = Single
        exclude = ('slug',)

    image = forms.ImageField(label='Image', required=True,
                             widget=ItemCustomClearableFileInput)
    video_url = forms.CharField(label='Youtube embed link*')
