from django import forms
from .models import Price, Service
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from .widgets import CustomClearableFileInput
from django.forms.models import inlineformset_factory


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
            'description': 'Description',
        }

        self.fields['image'].widget = CustomClearableFileInput()
        for field in self.fields:
            if field != 'image' and field != 'offer':
                self.fields[field].widget.attrs[
                    'placeholder'] = f'{placeholders[field]} *'
                self.fields[field].label = False


class PriceForm(forms.ModelForm):

    class Meta:
        model = Price
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Adds classes to the form. Code for setting the form_class, field_class
        and label_class is from
        https://django-crispy-forms.readthedocs.io/en/latest/form_helper.html
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('price', css_class='col'),
                Column('size', css_class='col'),
                Column('DELETE', css_class='col-auto'),
                css_class='row mb-3',
            )
        )
        self.helper.form_tag = False

        for field in self.fields:
            if field == 'price':
                self.fields[field].widget.attrs[
                    'placeholder'] = 'Price *'
            self.fields[field].label = False


class AppointmentForm(forms.Form):
    APPOINTMENT_CHOICES = [('', 'Time *'), ]
    SIZE_CHOICES = [
        ('', 'Dog Size *'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    appointments = forms.ChoiceField(choices=APPOINTMENT_CHOICES)
    sizes = forms.ChoiceField(choices=SIZE_CHOICES)
    comments = forms.CharField(widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes andremove auto-generated
        labels
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'mb-3'
        self.fields['comments'].widget.attrs = {
            'placeholder': 'Comments *',
            'rows': '8',
        }
        for field in self.fields:
            if field != 'comments':
                self.fields[field].widget.attrs['class'] = 'form-select'
            self.fields[field].label = False


PriceFormSet = inlineformset_factory(Service, Price, form=PriceForm, extra=1)
