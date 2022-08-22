import imp
from django import forms 
from .models import Meaurements

class MeasureForms(forms.ModelForm):
    class Meta:
        model = Meaurements
        fields = ('destination',)