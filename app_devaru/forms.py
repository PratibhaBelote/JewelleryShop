from django import forms
from .models import JewelleryItem


class JewelleryItemForm(forms.ModelForm):
    class Meta:
        model = JewelleryItem
        fields = ['category', 'name', 'quantity']



from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'product','category', 'phone', 'quantity', 'amount', 'status']
