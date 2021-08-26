from django import forms
from .models import Comment, Single
from shop.widgets import GeneralCustomClearableFileInput


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class AddSingleForm(forms.ModelForm):
    class Meta:
        model = Single
        exclude = ('slug',)

    image = forms.ImageField(label='', required=True,
                             widget=GeneralCustomClearableFileInput)
    video_url = forms.URLField(required=True, label="Video URL - (src attibute \
                                                from the Youtube embed code)")
