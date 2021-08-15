from django import forms
from .models import Pet
from crispy_forms.helper import FormHelper


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        exclude = ('user_profile',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-3'
        placeholders = {
            'name': 'Name',
        }

        for field in self.fields:
            if field != 'breed':
                placeholder = f'{placeholders[field]} *'
                self.fields[field].widget.attrs['placeholder'] = placeholder
            else:
                self.fields[field].empty_label = 'Breed *'
                self.fields[field].widget.attrs['class'] = 'form-select'
            self.fields[field].label = False
