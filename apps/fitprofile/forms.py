from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import FitProfile
from django import forms

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
        

class ProfileForm(ModelForm):
    class Meta:
       
        model = FitProfile
        fields = ['fit_prof_phne','fit_prof_birth_date','fit_prof_height','fit_prof_weight','fit_sexo']
  