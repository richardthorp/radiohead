from django import forms
from shop.widgets import GeneralCustomClearableFileInput
from .models import PortalImagesPost, PortalTextPost, PortalVideoPost
from .widgets import ImagesPostCustomClearableFileInput


class AddTextPostForm(forms.ModelForm):
    class Meta:
        model = PortalTextPost
        exclude = ('slug', 'text',)
        labels = {
            'text_content': 'Text (as HTML)'
        }

    lead_image = forms.ImageField(required=True, label="",
                                  widget=GeneralCustomClearableFileInput)

    # Add classes to form init method credit - Christian Abbott
    # https://stackoverflow.com/questions/29716023/add-class-to-form-field-django-modelform
    def __init__(self, *args, **kwargs):
        super(AddTextPostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def __str__(self):
        return 'AddTextPostForm'


class AddVideoPostForm(forms.ModelForm):
    class Meta:
        model = PortalVideoPost
        exclude = ('slug', 'video',)
        labels = {
            'text_content': 'Text (as HTML)'
        }

    lead_image = forms.ImageField(required=True, label='',
                                  widget=GeneralCustomClearableFileInput)
    video_url = forms.URLField(required=True, label="Video URL - (src attibute \
                                                from the Youtube embed code)")

    # Add classes to form init method credit - Christian Abbott
    # https://stackoverflow.com/questions/29716023/add-class-to-form-field-django-modelform
    def __init__(self, *args, **kwargs):
        super(AddVideoPostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def __str__(self):
        return 'AddVideoPostForm'


class AddImagesPostForm(forms.ModelForm):
    class Meta:
        model = PortalImagesPost
        exclude = ('slug',)
        labels = {
            'text_content': 'Text (as HTML)'
        }

    lead_image = forms.ImageField(required=True, label='',
                                  widget=GeneralCustomClearableFileInput)
    image_1 = forms.ImageField(required=True, label='',
                               widget=ImagesPostCustomClearableFileInput)
    image_2 = forms.ImageField(required=True, label='',
                               widget=ImagesPostCustomClearableFileInput)
    image_3 = forms.ImageField(required=False, label='',
                               widget=ImagesPostCustomClearableFileInput)
    image_4 = forms.ImageField(required=False, label='',
                               widget=ImagesPostCustomClearableFileInput)
    image_5 = forms.ImageField(required=False, label='',
                               widget=ImagesPostCustomClearableFileInput)
    image_6 = forms.ImageField(required=False, label='',
                               widget=ImagesPostCustomClearableFileInput)
    image_7 = forms.ImageField(required=False, label='',
                               widget=ImagesPostCustomClearableFileInput)
    image_8 = forms.ImageField(required=False, label='',
                               widget=ImagesPostCustomClearableFileInput)

    # Add classes to form init method credit - Christian Abbott
    # https://stackoverflow.com/questions/29716023/add-class-to-form-field-django-modelform
    def __init__(self, *args, **kwargs):
        super(AddImagesPostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def __str__(self):
        return 'AddImagesPostForm'
