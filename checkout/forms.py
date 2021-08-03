from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'email',
            'name',
            'phone_number',
            'address_line1',
            'address_line2',
            'town_or_city',
            'postcode',
            'country',
            )
    address_line1 = forms.CharField(label='Address Line 1')
    address_line2 = forms.CharField(label='Address Line 2')
