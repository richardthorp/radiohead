from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


# Custom Clearable File Input code copied from Boutique Ado project
# CREDIT - Chris Zielinski
class ProfileCustomClearableFileInput(ClearableFileInput):
    clear_checkbox_label = _('Remove')
    initial_text = _('Current image')
    input_text = _('')
    template_name = 'profiles/custom_widget_templates/profile_custom_clearable_file_input.html'
