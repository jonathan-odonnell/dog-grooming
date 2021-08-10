from django import forms
from crispy_forms.helper import FormHelper


class NewsletterEmailForm(forms.Form):
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes andremove auto-generated
        labels
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-3'
        placeholders = {
            'subject': 'Subject',
            'message': 'Message',
        }

        for field in self.fields:
            if field == 'message':
                self.fields[field].widget.attrs['rows'] = '8'
            self.fields[field].widget.attrs[
                    'placeholder'] = f'{placeholders[field]} *'
            self.fields[field].label = False
