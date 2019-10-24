from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user', 'pub_date', 'profile']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user','score']

class ReviewForm(forms.ModelForm):
    class Meta:
        model =Review
        exclude= ['user','project']