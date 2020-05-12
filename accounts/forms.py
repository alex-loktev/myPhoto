from django import forms
from django.contrib.auth.models import User
from .models import *
from posts.models import Post


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] == cd['password2']:
            return cd['password2']
        else:
            return forms.ValidationError('Password don\'t match')


class SettingForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'name', 'surname', 'description')


class PostAddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('image', 'description',)

