from django.forms import ModelForm
from .models import Comment, Single


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class AddSingleForm(ModelForm):
    class Meta:
        model = Single
        fields = '__all__'

