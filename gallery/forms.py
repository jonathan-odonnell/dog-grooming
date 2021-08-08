from django import forms
from .models import Image
from crispy_forms.helper import FormHelper
from services.widgets import CustomClearableFileInput


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes and remove auto-generated
        labels
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-3'
        self.fields['image'].widget = CustomClearableFileInput()
        for field in self.fields:
            if field != 'image':
                self.fields[field].widget.attrs[
                    'placeholder'] = 'Name'
            self.fields[field].label = False
