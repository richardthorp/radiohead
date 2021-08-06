from django import forms
from .models import Comment, Single


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class AddSingleForm(forms.ModelForm):
    class Meta:
        model = Single
        exclude = ('slug',)

    video_url = forms.CharField(label='Youtube embed link*')
