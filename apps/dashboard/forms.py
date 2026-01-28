from django.forms import ModelForm
from .models import Dashboard

class PesoForm(ModelForm):
    class Meta:
        model = Dashboard
        fields = ['fit_fcregister','fit_weight','fit_observation']