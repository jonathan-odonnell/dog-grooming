from django import forms
from .models import Contact
from crispy_forms.helper import FormHelper


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ('user_profile', 'date',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes and removes auto-generated
        labels
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-3'
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'subject': 'Subject',
            'message': 'Message',
        }

        for field in self.fields:
            self.fields[field].widget.attrs[
                'placeholder'] = f'{placeholders[field]} *'
            self.fields[field].label = False
