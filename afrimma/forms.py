from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class UploadForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('design', 'usability', 'creativity', 'content', 'overall', 'posted', 'user' )



class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        exclude=['overall_score','profile','project']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_photo', 'bio', 'contact')

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
