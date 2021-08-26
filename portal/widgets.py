from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


# Custom Clearable File Input code copied from Boutique Ado project
class ImagesPostCustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = _('Remove')
    initial_text = _('Current image')
    input_text = _('')
    template_name = 'portal/custom_widget_templates/images_post_custom_clearable_file_input.html'
