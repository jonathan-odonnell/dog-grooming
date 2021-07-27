from django import forms
from .models import Service
from crispy_forms.helper import FormHelper


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes andremove auto-generated
        labels
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-3'
        placeholders = {
            'name': 'Name',
            'price': 'Price',
            'description': 'Description',
        }

        for field in self.fields:
            if field != 'offer':
                self.fields[field].widget.attrs[
                    'placeholder'] = f'{placeholders[field]} *'
                self.fields[field].label = False
